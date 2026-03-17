const API_BASE = import.meta.env.VITE_API_URL || 'https://backend-api-production-ab9c.up.railway.app/api/v1';

interface RequestOptions {
	method?: string;
	body?: unknown;
	token?: string;
	apiKey?: string;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
	const { method = 'GET', body, token, apiKey } = options;

	const headers: Record<string, string> = {
		'Content-Type': 'application/json'
	};

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}
	if (apiKey) {
		headers['X-API-Key'] = apiKey;
	}

	const res = await fetch(`${API_BASE}${endpoint}`, {
		method,
		headers,
		body: body ? JSON.stringify(body) : undefined
	});

	if (!res.ok) {
		const error = await res.json().catch(() => ({ detail: 'Request failed' }));
		throw new Error(error.detail || `HTTP ${res.status}`);
	}

	if (res.status === 204) return undefined as T;
	return res.json();
}

export const api = {
	// Auth
	register: (data: { email: string; password: string; company_name?: string }) =>
		request('/auth/register', { method: 'POST', body: data }),

	login: (data: { email: string; password: string }) =>
		request<{ access_token: string; merchant: any }>('/auth/login', { method: 'POST', body: data }),

	refresh: (token: string) =>
		request<{ access_token: string; merchant: any }>('/auth/refresh', { method: 'POST', token }),

	// Merchant
	getMe: (token: string) => request<any>('/merchant/me', { token }),

	updateMe: (token: string, data: any) =>
		request<any>('/merchant/me', { method: 'PATCH', token, body: data }),

	rollApiKeys: (token: string) =>
		request<any>('/merchant/api-keys/roll', { method: 'POST', token }),

	// Payments
	listPayments: (apiKey: string, params?: string) =>
		request<any[]>(`/payments${params ? `?${params}` : ''}`, { apiKey }),

	getPayment: (apiKey: string, id: string) =>
		request<any>(`/payments/${id}`, { apiKey }),

	createPayment: (apiKey: string, data: any) =>
		request<any>('/payments/create', { method: 'POST', apiKey, body: data }),

	// Payment Links
	listPaymentLinks: (apiKey: string) =>
		request<any[]>('/payment-links', { apiKey }),

	createPaymentLink: (apiKey: string, data: any) =>
		request<any>('/payment-links', { method: 'POST', apiKey, body: data }),

	// Subscriptions
	listSubscriptions: (apiKey: string) =>
		request<any[]>('/subscriptions', { apiKey }),

	createSubscription: (apiKey: string, data: any) =>
		request<any>('/subscriptions', { method: 'POST', apiKey, body: data }),

	// Analytics
	getOverview: (apiKey: string, params?: string) =>
		request<any>(`/analytics/overview${params ? `?${params}` : ''}`, { apiKey }),

	getByChain: (apiKey: string) => request<any[]>('/analytics/by-chain', { apiKey }),

	getByToken: (apiKey: string) => request<any[]>('/analytics/by-token', { apiKey }),

	// Webhooks
	listWebhookEvents: (apiKey: string) => request<any[]>('/webhooks/events', { apiKey }),

	sendTestWebhook: (apiKey: string) =>
		request<any>('/webhooks/test', { method: 'POST', apiKey, body: {} }),

	// Payouts
	listPayouts: (apiKey: string) => request<any[]>('/payouts', { apiKey }),

	requestPayout: (apiKey: string, data: any) =>
		request<any>('/payouts/request', { method: 'POST', apiKey, body: data })
};
