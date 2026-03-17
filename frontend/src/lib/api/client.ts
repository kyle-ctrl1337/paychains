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

	// Payments (accept token or apiKey)
	listPayments: (auth: string, params?: string) =>
		request<any[]>(`/payments${params ? `?${params}` : ''}`, auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	getPayment: (auth: string, id: string) =>
		request<any>(`/payments/${id}`, auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	createPayment: (auth: string, data: any) =>
		request<any>('/payments/create', { method: 'POST', body: data, ...(auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }) }),

	// Payment Links
	listPaymentLinks: (auth: string) =>
		request<any[]>('/payment-links', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	createPaymentLink: (auth: string, data: any) =>
		request<any>('/payment-links', { method: 'POST', body: data, ...(auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }) }),

	// Subscriptions
	listSubscriptions: (auth: string) =>
		request<any[]>('/subscriptions', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	createSubscription: (auth: string, data: any) =>
		request<any>('/subscriptions', { method: 'POST', body: data, ...(auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }) }),

	// Analytics
	getOverview: (auth: string, params?: string) =>
		request<any>(`/analytics/overview${params ? `?${params}` : ''}`, auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	getByChain: (auth: string) =>
		request<any[]>('/analytics/by-chain', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	getByToken: (auth: string) =>
		request<any[]>('/analytics/by-token', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	// Webhooks
	listWebhookEvents: (auth: string) =>
		request<any[]>('/webhooks/events', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	sendTestWebhook: (auth: string) =>
		request<any>('/webhooks/test', { method: 'POST', body: {}, ...(auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }) }),

	// Payouts
	listPayouts: (auth: string) =>
		request<any[]>('/payouts', auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }),

	requestPayout: (auth: string, data: any) =>
		request<any>('/payouts/request', { method: 'POST', body: data, ...(auth.startsWith('pc_') ? { apiKey: auth } : { token: auth }) }),

	// Admin
	adminStats: (token: string) => request<any>('/admin/stats', { token }),

	adminMerchants: (token: string) => request<any[]>('/admin/merchants', { token }),

	adminPayments: (token: string) => request<any[]>('/admin/payments', { token }),

	adminUpdateMerchant: (token: string, merchantId: string, data: any) =>
		request<any>(`/admin/merchants/${merchantId}`, { method: 'PATCH', token, body: data })
};
