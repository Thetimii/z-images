# Supabase Setup Instructions

## 1. Create Storage Bucket

1. Go to your Supabase Dashboard → **Storage**
2. Click **New bucket**
3. Settings:
   - **Name**: `generated-images`
   - **Public**: ✅ Yes (so images are accessible via URL)
   - **File size limit**: 10 MB
   - **Allowed MIME types**: `image/png`, `image/jpeg`

## 2. Run SQL Schema

1. Go to **SQL Editor** in Supabase Dashboard
2. Copy and paste the contents of `schema.sql`
3. Click **Run**

## 3. Get Your Credentials

1. Go to **Settings** → **API**
2. Copy:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **service_role key** (NOT the anon key - you need the service role for storage uploads)

## 4. Set Environment Variables in RunPod

In your RunPod Endpoint configuration, add these environment variables:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
API_KEY=your_secret_password
```

## 5. Test the Endpoint

```bash
curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "input": {
      "prompt": "A futuristic city with neon lights",
      "api_key": "your_secret_password",
      "user_id": "user_123"
    }
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "image_url": "https://xxxxx.supabase.co/storage/v1/object/public/generated-images/images/20260113_075500_abc123.png",
  "storage_path": "images/20260113_075500_abc123.png",
  "prompt": "A futuristic city with neon lights"
}
```

## Database Schema

The `generated_images` table stores:
- `id`: UUID (auto-generated)
- `prompt`: The text prompt used
- `image_url`: Public URL to the image
- `storage_path`: Path in Supabase Storage
- `num_inference_steps`: Number of steps used
- `guidance_scale`: Guidance scale used
- `created_at`: Timestamp
- `user_id`: Optional user identifier
- `job_id`: RunPod job ID

## Querying Images

```sql
-- Get all images
SELECT * FROM generated_images ORDER BY created_at DESC;

-- Get images by user
SELECT * FROM generated_images WHERE user_id = 'user_123';

-- Get recent images
SELECT * FROM generated_images WHERE created_at > NOW() - INTERVAL '24 hours';
```
