import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
	id: string;
	message: string;
	type: ToastType;
	duration: number;
}

const MAX_TOASTS = 5;

function createToastStore() {
	const { subscribe, update } = writable<Toast[]>([]);

	function add(message: string, type: ToastType, duration = 4000) {
		const id = crypto.randomUUID();
		const toast: Toast = { id, message, type, duration };

		update((toasts) => {
			const next = [...toasts, toast];
			// Keep only the newest MAX_TOASTS
			return next.length > MAX_TOASTS ? next.slice(next.length - MAX_TOASTS) : next;
		});

		if (duration > 0) {
			setTimeout(() => remove(id), duration);
		}

		return id;
	}

	function remove(id: string) {
		update((toasts) => toasts.filter((t) => t.id !== id));
	}

	return {
		subscribe,
		success: (message: string, duration?: number) => add(message, 'success', duration),
		error: (message: string, duration?: number) => add(message, 'error', duration),
		info: (message: string, duration?: number) => add(message, 'info', duration),
		warning: (message: string, duration?: number) => add(message, 'warning', duration),
		remove
	};
}

export const toast = createToastStore();
