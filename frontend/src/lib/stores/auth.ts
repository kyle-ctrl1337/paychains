import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface Merchant {
	id: string;
	email: string;
	company_name: string | null;
	plan: string;
	webhook_url: string | null;
	auto_convert_to: string;
	settlement_address: Record<string, string>;
	is_active: boolean;
	is_admin: boolean;
}

interface AuthState {
	token: string | null;
	merchant: Merchant | null;
	apiKeyLive: string | null;
	apiKeyTest: string | null;
}

const initialState: AuthState = {
	token: browser ? localStorage.getItem('pc_token') : null,
	merchant: browser ? JSON.parse(localStorage.getItem('pc_merchant') || 'null') : null,
	apiKeyLive: browser ? localStorage.getItem('pc_api_key_live') : null,
	apiKeyTest: browser ? localStorage.getItem('pc_api_key_test') : null
};

export const auth = writable<AuthState>(initialState);

export function setAuth(token: string, merchant: Merchant, apiKeyLive?: string, apiKeyTest?: string) {
	// Preserve existing stored keys if no new ones provided
	const existingLive = apiKeyLive || (browser ? localStorage.getItem('pc_api_key_live') : null);
	const existingTest = apiKeyTest || (browser ? localStorage.getItem('pc_api_key_test') : null);
	const state: AuthState = { token, merchant, apiKeyLive: existingLive, apiKeyTest: existingTest };
	auth.set(state);
	if (browser) {
		localStorage.setItem('pc_token', token);
		localStorage.setItem('pc_merchant', JSON.stringify(merchant));
		if (existingLive) localStorage.setItem('pc_api_key_live', existingLive);
		if (existingTest) localStorage.setItem('pc_api_key_test', existingTest);
	}
}

export function clearAuth() {
	auth.set({ token: null, merchant: null, apiKeyLive: null, apiKeyTest: null });
	if (browser) {
		localStorage.removeItem('pc_token');
		localStorage.removeItem('pc_merchant');
		localStorage.removeItem('pc_api_key_live');
		localStorage.removeItem('pc_api_key_test');
	}
}
