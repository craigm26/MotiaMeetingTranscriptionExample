/**
 * Meeting Transcription Processor Step
 * 
 * This step demonstrates how to create an event handler in Motia that:
 * 1. Subscribes to events from the API step
 * 2. Processes data asynchronously
 * 3. Updates real-time streams with progress
 * 4. Handles errors gracefully
 * 5. Emits completion events
 * 
 * In a real implementation, this would integrate with Whisper API
 * For this example, we simulate the transcription process
 */

import { EventConfig, Handlers } from 'motia'
import { z } from 'zod'

export const config: EventConfig = {
  type: 'event',
  name: 'MeetingTranscriptionProcessor',
  description: 'Processes meeting transcription requests with real-time streaming updates',

  /**
   * This step subscribes to events from the MeetingTranscriptionAPI
   * When the API receives a request, it emits a 'meeting-transcription' event
   * This step picks up that event and processes it asynchronously
   */
  subscribes: ['meeting-transcription'],

  /**
   * This step emits events when transcription is completed or fails
   * These events can be picked up by other steps for further processing
   */
  emits: ['transcription-completed', 'transcription-failed'],

  /**
   * Input schema defines the expected structure of incoming events
   */
  input: z.object({ 
    filename: z.string().describe('Name of the audio file to transcribe'),
    audioData: z.string().optional().describe('Base64 encoded audio data'),
    language: z.string().describe('Language code for transcription'),
    model: z.string().describe('Whisper model to use'),
    transcriptionId: z.string().describe('Unique ID for tracking this transcription'),
    apiRequest: z.boolean().optional().describe('Whether this came from an API request'),
    localWhisperPath: z.string().optional().describe('Path to local Whisper script')
  }),

  /**
   * The flows this step belongs to
   */
  flows: ['meeting-transcription'],
}

export const handler: Handlers['MeetingTranscriptionProcessor'] = async (input, { traceId, logger, emit, streams }) => {
  logger.info('Starting meeting transcription processing', { input })

  try {
    // Update stream with transcription start
    await streams.meetingTranscription.set(traceId, input.transcriptionId, {
      status: 'transcribing',
      progress: 10,
      filename: input.filename,
      localWhisperStatus: 'initializing',
      whisperModel: input.model,
      timestamp: new Date().toISOString()
    })

    /**
     * Simulate transcription process with progress updates
     * In a real implementation, this would:
     * 1. Call the local Whisper API
     * 2. Process the audio file
     * 3. Generate the transcript
     * 4. Extract metadata (duration, participants, etc.)
     */
    const transcriptionSteps = [
      { progress: 20, message: 'Loading Whisper model', whisperStatus: 'loading_model' },
      { progress: 40, message: 'Processing audio file', whisperStatus: 'processing_audio' },
      { progress: 60, message: 'Generating transcript', whisperStatus: 'generating_transcript' },
      { progress: 80, message: 'Post-processing results', whisperStatus: 'post_processing' },
      { progress: 90, message: 'Finalizing transcription', whisperStatus: 'finalizing' }
    ]

    const startTime = Date.now()

    // Simulate processing steps with delays
    for (const step of transcriptionSteps) {
      // In real implementation, this would be actual processing time
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Update stream with current progress
      await streams.meetingTranscription.set(traceId, input.transcriptionId, {
        status: 'transcribing',
        progress: step.progress,
        filename: input.filename,
        localWhisperStatus: step.whisperStatus,
        whisperModel: input.model,
        timestamp: new Date().toISOString()
      })
    }

    /**
     * Simulate transcription results
     * In a real implementation, this would come from the Whisper API
     */
    const mockTranscript = `This is a simulated transcript for ${input.filename}. 
    In a real implementation, this would be the actual transcription from the Whisper API.
    The transcript would include all spoken content with proper punctuation and formatting.`

    const mockDuration = Math.floor(Math.random() * 3600) + 300 // 5-65 minutes
    const mockParticipants = ['John Doe', 'Jane Smith', 'Bob Johnson']
    const mockActionItems = [
      'Schedule follow-up meeting',
      'Review project timeline',
      'Update documentation'
    ]

    const processingTime = Date.now() - startTime

    // Update stream with completion
    await streams.meetingTranscription.set(traceId, input.transcriptionId, {
      status: 'completed',
      progress: 100,
      filename: input.filename,
      duration: mockDuration,
      transcript: mockTranscript,
      participants: mockParticipants,
      actionItems: mockActionItems,
      localWhisperStatus: 'completed',
      whisperModel: input.model,
      processingTime,
      timestamp: new Date().toISOString()
    })

    logger.info('Meeting transcription completed successfully', { 
      filename: input.filename,
      transcriptionId: input.transcriptionId,
      duration: mockDuration,
      processingTime,
      whisperModel: input.model
    })

    /**
     * Emit completion event
     * This can be picked up by other steps for further processing
     * (e.g., analysis, storage, notification)
     */
    await emit({
      topic: 'transcription-completed',
      data: { 
        filename: input.filename,
        transcriptionId: input.transcriptionId,
        duration: mockDuration,
        transcript: mockTranscript,
        participants: mockParticipants,
        actionItems: mockActionItems,
        processingTime,
        whisperModel: input.model,
        timestamp: new Date().toISOString()
      }
    })

  } catch (error) {
    logger.error('Meeting transcription failed', { 
      error: error instanceof Error ? error.message : String(error),
      filename: input.filename,
      transcriptionId: input.transcriptionId
    })

    // Update stream with error status
    await streams.meetingTranscription.set(traceId, input.transcriptionId, {
      status: 'failed',
      progress: 0,
      filename: input.filename,
      error: error instanceof Error ? error.message : String(error),
      localWhisperStatus: 'failed',
      whisperModel: input.model,
      timestamp: new Date().toISOString()
    })

    /**
     * Emit failure event
     * This can be picked up by error handling steps
     */
    await emit({
      topic: 'transcription-failed',
      data: { 
        filename: input.filename,
        transcriptionId: input.transcriptionId,
        error: error instanceof Error ? error.message : String(error),
        whisperModel: input.model,
        timestamp: new Date().toISOString()
      }
    })
  }
} 