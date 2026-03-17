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
		pending: 'bg-yellow-100 text-yellow-800',
		confirming: 'bg-blue-100 text-blue-800',
		completed: 'bg-green-100 text-green-800',
		failed: 'bg-red-100 text-red-800',
		expired: 'bg-gray-100 text-gray-800',
		refunded: 'bg-purple-100 text-purple-800',
		active: 'bg-green-100 text-green-800',
		paused: 'bg-yellow-100 text-yellow-800',
		cancelled: 'bg-red-100 text-red-800',
		past_due: 'bg-orange-100 text-orange-800',
		delivered: 'bg-green-100 text-green-800'
	};
	return colors[status] || 'bg-gray-100 text-gray-800';
}
