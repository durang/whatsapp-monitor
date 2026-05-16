# EBS Encryption Swap — Procedure (run from Sergio's Mac)

**Estado actual (2026-05-16):**
- ✅ EBS default encryption habilitado a nivel cuenta (nuevos volúmenes encriptados auto)
- ✅ Snapshot creado: `snap-082538e444ef4b0b9` (60GB, completed 100%)
- 🔴 Volumen actual `vol-06c0e214b6bdb333b` aún unencrypted

**Por qué desde Mac:** este script para la EC2 que está corriendo este código → no puede ejecutarse desde adentro.

## Pre-flight

```bash
# Desde Mac, asegurate que AWS CLI tiene las credenciales sergio-admin
aws sts get-caller-identity
# Debería retornar arn:aws:iam::771713467764:user/sergio-admin
```

## Procedure (downtime ~5-10 min)

```bash
INSTANCE_ID=i-05dc3b94239d923a6
OLD_VOLUME=vol-06c0e214b6bdb333b
SNAPSHOT_ID=snap-082538e444ef4b0b9
REGION=us-east-1
AZ=us-east-1c

# 1. Verificar snapshot está completed
aws ec2 describe-snapshots --snapshot-ids $SNAPSHOT_ID --region $REGION \
  --query 'Snapshots[0].[State,Progress]' --output text
# → completed 100%

# 2. Crear volumen ENCRIPTADO desde el snapshot
# (default encryption está ON → el nuevo será encrypted)
NEW_VOLUME=$(aws ec2 create-volume \
  --snapshot-id $SNAPSHOT_ID \
  --availability-zone $AZ \
  --volume-type gp3 \
  --encrypted \
  --tag-specifications "ResourceType=volume,Tags=[{Key=Name,Value=jarvis-v3-root-encrypted},{Key=Backup,Value=daily}]" \
  --region $REGION \
  --query VolumeId --output text)
echo "New volume: $NEW_VOLUME"

# 3. Esperar a que esté available
aws ec2 wait volume-available --volume-ids $NEW_VOLUME --region $REGION
aws ec2 describe-volumes --volume-ids $NEW_VOLUME --region $REGION \
  --query 'Volumes[0].[State,Encrypted]' --output text
# → available True

# 4. STOP la instancia (avisar usuarios antes — Hermes/OpenClaw bajan)
aws ec2 stop-instances --instance-ids $INSTANCE_ID --region $REGION
aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID --region $REGION

# 5. Detach volumen viejo
aws ec2 detach-volume --volume-id $OLD_VOLUME --region $REGION
aws ec2 wait volume-available --volume-ids $OLD_VOLUME --region $REGION

# 6. Attach volumen nuevo COMO /dev/xvda (root)
aws ec2 attach-volume \
  --volume-id $NEW_VOLUME \
  --instance-id $INSTANCE_ID \
  --device /dev/xvda \
  --region $REGION

# 7. Start instancia
aws ec2 start-instances --instance-ids $INSTANCE_ID --region $REGION
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

# 8. Verificar SSH + servicios
ssh ec2-user@54.211.99.214 'systemctl is-active openclaw-gateway tailscaled cloudflared'
ssh ec2-user@54.211.99.214 'curl -s http://127.0.0.1:3000/health'

# 9. Verificar encryption
aws ec2 describe-volumes --filters "Name=attachment.instance-id,Values=$INSTANCE_ID" \
  --region $REGION --query 'Volumes[].[VolumeId,Encrypted]' --output text
# → debería mostrar Encrypted=True

# 10. Tag para DLM backup
aws ec2 create-tags --resources $NEW_VOLUME \
  --tags Key=Backup,Value=daily Key=Name,Value=jarvis-v3-root-encrypted \
  --region $REGION

# 11. (Opcional) Borrar volumen viejo después de 7 días de operación estable
# aws ec2 delete-volume --volume-id $OLD_VOLUME --region $REGION
```

## Verificación post-swap (desde la EC2)

```bash
# Lie-detector ahora debería pasar 22/22 (era 21/22)
bash /home/ec2-user/.openclaw/skills/gbrain/run.sh verify | grep "Lie-detector"
# → "Lie-detector: 22/22"
```

## Rollback (si algo sale mal)

```bash
# 1. Stop instance
aws ec2 stop-instances --instance-ids $INSTANCE_ID --region $REGION
aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID --region $REGION

# 2. Detach volumen nuevo
aws ec2 detach-volume --volume-id $NEW_VOLUME --region $REGION

# 3. Re-attach volumen viejo
aws ec2 attach-volume --volume-id $OLD_VOLUME --instance-id $INSTANCE_ID \
  --device /dev/xvda --region $REGION

# 4. Start
aws ec2 start-instances --instance-ids $INSTANCE_ID --region $REGION
```

El volumen viejo NO se borra hasta confirmar que el nuevo funciona bien por días.
