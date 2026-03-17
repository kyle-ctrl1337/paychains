export function formatUSD(amount: number | string): string {
	const num = typeof amount === 'string' ? parseFloat(amount) : amount;
	return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);
}

export function formatCrypto(amount: number | string, decimals = 6): string {
	const num = typeof amount === 'string' ? parseFloat(amount) : amount;
	return num.toFixed(decimals);
}

export function formatDate(date: string): string {
	return new Intl.DateTimeFormat('en-US', {
		dateStyle: 'medium',
		timeStyle: 'short'
	}).format(new Date(date));
}

export function shortenAddress(address: string, chars = 6): string {
	if (!address) return '';
	return `${address.slice(0, chars + 2)}...${address.slice(-chars)}`;
}

export function statusColor(status: string): string {
	const colors: Record<string, string> = {
		pending: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
		confirming: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
		completed: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
		failed: 'bg-red-500/10 text-red-400 border border-red-500/20',
		expired: 'bg-surface-500/10 text-surface-400 border border-surface-500/20',
		refunded: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
		active: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
		paused: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
		cancelled: 'bg-red-500/10 text-red-400 border border-red-500/20',
		past_due: 'bg-orange-500/10 text-orange-400 border border-orange-500/20',
		delivered: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
		processing: 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
	};
	return colors[status] || 'bg-surface-500/10 text-surface-400 border border-surface-500/20';
}
