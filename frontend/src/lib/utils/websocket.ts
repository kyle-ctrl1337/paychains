export function createPaymentSocket(paymentId: string, onUpdate: (data: any) => void) {
	// WebSocket for real-time payment status updates
	// Will connect to backend WS endpoint in Phase 3
	const wsBase = import.meta.env.VITE_WS_URL || 'wss://api.paychains.dev';
	const wsUrl = `${wsBase}/ws/payments/${paymentId}`;

	let ws: WebSocket | null = null;
	let reconnectTimer: ReturnType<typeof setTimeout>;

	function connect() {
		ws = new WebSocket(wsUrl);

		ws.onmessage = (event) => {
			const data = JSON.parse(event.data);
			onUpdate(data);
		};

		ws.onclose = () => {
			// Reconnect after 3 seconds
			reconnectTimer = setTimeout(connect, 3000);
		};

		ws.onerror = () => {
			ws?.close();
		};
	}

	connect();

	return {
		close() {
			clearTimeout(reconnectTimer);
			ws?.close();
		}
	};
}
