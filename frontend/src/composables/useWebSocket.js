import { ref } from 'vue'

export function useWebSocket() {
  let ws = null
  const connected = ref(false)
  const messages = ref([])
  const relationship = ref(null)

  function connect(token) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const url = `${protocol}//${host}/api/chat`

    ws = new WebSocket(url)

    ws.onopen = () => {
      connected.value = true
      // Send auth token as first message
      ws.send(JSON.stringify({ token }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'connected') {
        console.log('Chat connected, conv_id:', data.conversation_id)
        return
      }

      if (data.type === 'error') {
        console.error('Chat error:', data.message)
        return
      }

      if (data.type === 'message') {
        messages.value.push({
          role: data.role,
          content: data.content,
          timestamp: new Date(),
        })
        if (data.relationship) {
          relationship.value = data.relationship
        }
      }
    }

    ws.onclose = () => {
      connected.value = false
    }

    ws.onerror = (err) => {
      console.error('WebSocket error:', err)
    }
  }

  function send(message) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      messages.value.push({
        role: 'user',
        content: message,
        timestamp: new Date(),
      })
      ws.send(JSON.stringify({ message }))
    }
  }

  function disconnect() {
    if (ws) {
      ws.close()
      ws = null
    }
    connected.value = false
  }

  return { connected, messages, relationship, connect, send, disconnect }
}
