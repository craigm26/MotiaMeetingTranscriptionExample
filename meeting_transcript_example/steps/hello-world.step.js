/**
 * Hello World API Step - Meeting Transcription Example
 * 
 * This is a simple API step that demonstrates basic Motia API functionality.
 * It's included as a starting point for understanding how Motia steps work.
 */

exports.config = {
  type: 'api', // "event", "api", or "cron"
  path: '/hello-world',
  method: 'GET',
  name: 'HelloWorld',
  description: 'Simple API endpoint to test the meeting transcription system',
  emits: [],
  flows: ['meeting-transcription'],
}

exports.handler = async () => {
  return {
    status: 200,
    body: { 
      message: 'Hello from Motia Meeting Transcription System!',
      endpoints: {
        'GET /hello-world': 'This endpoint - system status',
        'POST /transcribe-meeting': 'Start a meeting transcription',
        'GET /local-status': 'Check local system status'
      },
      documentation: 'See README.md for usage instructions'
    },
  }
}