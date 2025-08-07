/**
 * Meeting Transcription Stream Configuration
 * 
 * This stream provides real-time updates during meeting transcription.
 * It demonstrates how to:
 * 1. Define a stream schema using Zod
 * 2. Structure real-time data updates
 * 3. Track progress and status
 * 4. Handle errors and metadata
 */

import { StreamConfig } from 'motia'
import { z } from 'zod'

export const config: StreamConfig = {
  /**
   * Stream name - this will be available as context.streams.meetingTranscription
   */
  name: 'meetingTranscription',
  
  /**
   * Schema defines the structure of stream records
   * This ensures type safety and provides documentation
   */
  schema: z.object({ 
    // Current status of the transcription process
    status: z.enum(['uploading', 'transcribing', 'processing', 'completed', 'failed']),
    
    // Progress percentage (0-100)
    progress: z.number().min(0).max(100),
    
    // Original filename being processed
    filename: z.string(),
    
    // Optional fields that are populated as processing progresses
    duration: z.number().optional().describe('Audio duration in seconds'),
    transcript: z.string().optional().describe('Generated transcript text'),
    summary: z.string().optional().describe('Meeting summary'),
    actionItems: z.array(z.string()).optional().describe('Extracted action items'),
    participants: z.array(z.string()).optional().describe('Meeting participants'),
    error: z.string().optional().describe('Error message if failed'),
    
    // Metadata
    timestamp: z.string().describe('ISO timestamp of this update'),
    localWhisperStatus: z.string().optional().describe('Status of Whisper processing'),
    whisperModel: z.string().optional().describe('Whisper model being used'),
    processingTime: z.number().optional().describe('Total processing time in milliseconds')
  }),

  /**
   * Base configuration for the stream
   */
  baseConfig: {
    /**
     * Use default storage to persist stream data
     * This allows clients to retrieve historical updates
     */
    storageType: 'default',
  },
} 