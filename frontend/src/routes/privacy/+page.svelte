<script>
	import Logo from '$lib/components/Logo.svelte';
</script>

<svelte:head>
	<title>Privacy Policy - PayChains</title>
</svelte:head>

<div class="min-h-screen bg-surface-950">
	<!-- Header -->
	<nav class="sticky top-0 z-50 border-b border-white/[0.06] bg-surface-950/90 backdrop-blur-xl">
		<div class="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
			<a href="/" class="flex items-center">
				<Logo size={28} textClass="text-[15px]" />
			</a>
			<a href="/" class="text-[13px] text-surface-400 hover:text-white transition-colors flex items-center gap-1.5">
				<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round"/></svg>
				Back to Home
			</a>
		</div>
	</nav>

	<!-- Content -->
	<main class="max-w-3xl mx-auto px-6 py-16 md:py-24">
		<div class="mb-12">
			<h1 class="text-3xl md:text-4xl font-bold tracking-tight text-white mb-3">Privacy Policy</h1>
			<p class="text-[14px] text-surface-500">Last updated: March 2026</p>
		</div>

		<div class="prose-legal space-y-10 text-[15px] leading-relaxed text-surface-300">

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">1. Introduction</h2>
				<p>PayChains ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our crypto payment processing platform, APIs, hosted checkout pages, dashboard, and related services (collectively, the "Service").</p>
				<p class="mt-3">By accessing or using the Service, you agree to the collection and use of information in accordance with this policy. If you do not agree, please discontinue use of the Service.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">2. Information We Collect</h2>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">2.1 Information You Provide</h3>
				<ul class="list-disc pl-6 space-y-2 text-surface-400">
					<li><span class="text-surface-300">Account information:</span> name, email address, password, and organization details when you register for an account.</li>
					<li><span class="text-surface-300">Payment and billing data:</span> wallet addresses, transaction amounts, token types, chain preferences, and billing contact details.</li>
					<li><span class="text-surface-300">API credentials:</span> API keys, webhook URLs, and integration configuration data.</li>
					<li><span class="text-surface-300">Communications:</span> information you provide when contacting our support team or submitting feedback.</li>
				</ul>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">2.2 Information Collected Automatically</h3>
				<ul class="list-disc pl-6 space-y-2 text-surface-400">
					<li><span class="text-surface-300">Usage data:</span> API call logs, request/response metadata, timestamps, endpoints accessed, and error rates.</li>
					<li><span class="text-surface-300">Device and browser information:</span> IP address, browser type and version, operating system, device identifiers, and screen resolution.</li>
					<li><span class="text-surface-300">Blockchain data:</span> on-chain transaction hashes, block confirmations, wallet addresses, token transfer amounts, and network identifiers. Note that blockchain transactions are inherently public.</li>
				</ul>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">2.3 Information from Third Parties</h3>
				<p class="text-surface-400">We may receive information from blockchain networks and public data sources to help monitor transactions, detect fraud, and improve our Service. PayChains does not perform identity verification (KYC) on merchants or their customers.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">3. How We Use Your Information</h2>
				<p>We use the information we collect for the following purposes:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>To provide, operate, and maintain the Service, including processing payments, generating deposit addresses, and delivering webhook notifications.</li>
					<li>To manage your account, authenticate access, and issue API credentials.</li>
					<li>To monitor blockchain networks for transaction confirmations and payment status updates.</li>
					<li>To process billing, calculate transaction fees, and generate invoices.</li>
					<li>To detect, prevent, and address fraud, abuse, security incidents, and technical issues.</li>
					<li>To comply with applicable legal obligations where required by law.</li>
					<li>To communicate with you about service updates, security alerts, and support inquiries.</li>
					<li>To analyze usage patterns and improve the performance, reliability, and features of the Service.</li>
				</ul>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">4. Cookies and Tracking Technologies</h2>
				<p>We use cookies and similar technologies to:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Essential cookies:</span> maintain your authenticated session and remember security preferences. These are required for the Service to function.</li>
					<li><span class="text-surface-300">Analytics cookies:</span> understand how users interact with our dashboard and documentation to improve the experience.</li>
					<li><span class="text-surface-300">Preference cookies:</span> remember your settings such as preferred chains, display currency, and theme.</li>
				</ul>
				<p class="mt-3 text-surface-400">You can manage cookie preferences through your browser settings. Disabling essential cookies may prevent you from using certain features of the Service.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">5. Third-Party Services</h2>
				<p>We may share information with the following categories of third-party service providers:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Blockchain networks:</span> transaction data is broadcast to and recorded on public blockchain networks (Ethereum, Polygon, BSC, Arbitrum, Base, and others) as an inherent part of processing payments.</li>
					<li><span class="text-surface-300">Cloud infrastructure providers:</span> for hosting, data storage, and content delivery.</li>
					<li><span class="text-surface-300">Analytics providers:</span> to help us understand usage patterns and improve the Service.</li>
					<li><span class="text-surface-300">Blockchain RPC providers:</span> for reading on-chain transaction data, confirming payments, and interacting with smart contracts.</li>
					<li><span class="text-surface-300">Communication providers:</span> for sending transactional emails, webhook deliveries, and support communications.</li>
				</ul>
				<p class="mt-3 text-surface-400">We require all third-party providers to handle your data in accordance with applicable data protection laws and our contractual obligations.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">6. Data Retention</h2>
				<p>We retain your information for as long as your account is active or as needed to provide the Service. Specifically:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Account data:</span> retained for the lifetime of your account plus 30 days after deletion request.</li>
					<li><span class="text-surface-300">Transaction records:</span> retained for a minimum of 5 years to comply with financial record-keeping obligations.</li>
					<li><span class="text-surface-300">API logs:</span> retained for 90 days for debugging and security analysis, then aggregated and anonymized.</li>
					<li><span class="text-surface-300">Blockchain data:</span> on-chain data is permanent and cannot be deleted due to the immutable nature of blockchain technology.</li>
				</ul>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">7. Data Security</h2>
				<p>We implement industry-standard security measures to protect your information, including:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>Encryption of data in transit (TLS 1.3) and at rest (AES-256).</li>
					<li>BIP-44 HD wallet derivation to ensure unique deposit addresses per payment with no address reuse.</li>
					<li>HMAC-SHA256 signature verification on all webhook deliveries.</li>
					<li>Regular security audits and penetration testing.</li>
					<li>Role-based access controls and multi-factor authentication for internal systems.</li>
				</ul>
				<p class="mt-3 text-surface-400">While we strive to protect your information, no method of electronic transmission or storage is 100% secure. We cannot guarantee absolute security.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">8. Your Rights</h2>
				<p>Depending on your jurisdiction, you may have the following rights regarding your personal data:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Access:</span> request a copy of the personal data we hold about you.</li>
					<li><span class="text-surface-300">Correction:</span> request correction of inaccurate or incomplete personal data.</li>
					<li><span class="text-surface-300">Deletion:</span> request deletion of your personal data, subject to our retention obligations.</li>
					<li><span class="text-surface-300">Portability:</span> request a machine-readable export of your data.</li>
					<li><span class="text-surface-300">Objection:</span> object to certain types of processing of your personal data.</li>
					<li><span class="text-surface-300">Restriction:</span> request that we limit processing of your personal data under certain circumstances.</li>
				</ul>
				<p class="mt-3 text-surface-400">To exercise any of these rights, please contact us at <a href="mailto:support@paychains.dev" class="text-brand-400 hover:text-brand-300 transition-colors">support@paychains.dev</a>. We will respond to your request within 30 days.</p>
				<p class="mt-3 text-surface-400">Please note that certain data, particularly on-chain blockchain transaction data, cannot be modified or deleted due to the immutable nature of distributed ledger technology.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">9. International Data Transfers</h2>
				<p class="text-surface-400">Your information may be transferred to and processed in countries other than your country of residence. We ensure appropriate safeguards are in place for such transfers in compliance with applicable data protection laws.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">10. Children's Privacy</h2>
				<p class="text-surface-400">The Service is not directed to individuals under the age of 18. We do not knowingly collect personal information from children. If we become aware that a child has provided us with personal data, we will take steps to delete such information.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">11. Changes to This Policy</h2>
				<p class="text-surface-400">We may update this Privacy Policy from time to time. We will notify you of material changes by posting the updated policy on this page and updating the "Last updated" date. Your continued use of the Service after any changes constitutes acceptance of the revised policy.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">12. Contact Us</h2>
				<p class="text-surface-400">If you have any questions about this Privacy Policy or our data practices, please contact us at:</p>
				<div class="mt-4 p-5 rounded-xl border border-white/[0.06] bg-white/[0.02]">
					<p class="text-white font-medium">PayChains</p>
					<p class="text-surface-400 mt-1">Email: <a href="mailto:support@paychains.dev" class="text-brand-400 hover:text-brand-300 transition-colors">support@paychains.dev</a></p>
				</div>
			</section>

			<div class="pt-8 border-t border-white/[0.06] text-[13px] text-surface-500">
				<p>See also our <a href="/terms" class="text-brand-400 hover:text-brand-300 transition-colors">Terms of Service</a>.</p>
			</div>
		</div>
	</main>
</div>
