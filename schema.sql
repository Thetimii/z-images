-- Create a table to store generated images metadata
CREATE TABLE IF NOT EXISTS generated_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt TEXT NOT NULL,
    image_url TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    num_inference_steps INTEGER DEFAULT 8,
    guidance_scale REAL DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id TEXT,
    job_id TEXT
);

-- Create an index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_generated_images_created_at ON generated_images(created_at DESC);

-- Create an index on user_id if you want to filter by user
CREATE INDEX IF NOT EXISTS idx_generated_images_user_id ON generated_images(user_id);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE generated_images ENABLE ROW LEVEL SECURITY;

-- Create a policy to allow authenticated users to read their own images
CREATE POLICY "Users can view their own images" ON generated_images
    FOR SELECT
    USING (auth.uid()::text = user_id OR user_id IS NULL);

-- Create a policy to allow the service role to insert (for the handler)
CREATE POLICY "Service role can insert images" ON generated_images
    FOR INSERT
    WITH CHECK (true);

-- Create the storage bucket for images (run this in Supabase Dashboard > Storage)
-- Bucket name: 'generated-images'
-- Public: true (so images are accessible via URL)
-- File size limit: 10MB
-- Allowed MIME types: image/png, image/jpeg
