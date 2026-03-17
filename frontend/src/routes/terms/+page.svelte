<svelte:head>
	<title>Terms of Service - PayChains</title>
</svelte:head>

<div class="min-h-screen bg-surface-950">
	<!-- Header -->
	<nav class="sticky top-0 z-50 border-b border-white/[0.06] bg-surface-950/90 backdrop-blur-xl">
		<div class="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
			<a href="/" class="flex items-center gap-2.5">
				<div class="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
					<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
						<polyline points="4 12 9 17 20 6" />
					</svg>
				</div>
				<span class="text-[15px] font-semibold tracking-[-0.01em]">PayChains</span>
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
			<h1 class="text-3xl md:text-4xl font-bold tracking-tight text-white mb-3">Terms of Service</h1>
			<p class="text-[14px] text-surface-500">Last updated: March 2026</p>
		</div>

		<div class="prose-legal space-y-10 text-[15px] leading-relaxed text-surface-300">

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">1. Acceptance of Terms</h2>
				<p>By accessing or using the PayChains platform, APIs, hosted checkout pages, dashboard, SDKs, documentation, and any related services (collectively, the "Service"), you agree to be bound by these Terms of Service ("Terms"). If you are using the Service on behalf of an organization, you represent that you have the authority to bind that organization to these Terms.</p>
				<p class="mt-3">If you do not agree to these Terms, you must not access or use the Service.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">2. Description of Service</h2>
				<p>PayChains provides a crypto payment processing platform that enables businesses to:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>Accept cryptocurrency payments across multiple blockchain networks, including Ethereum, Polygon, BSC, Arbitrum, and Base.</li>
					<li>Generate unique HD-wallet-derived deposit addresses for each payment.</li>
					<li>Create and manage recurring subscription billing in cryptocurrency.</li>
					<li>Auto-convert received tokens to stablecoins (USDC, USDT) at the time of payment.</li>
					<li>Receive real-time webhook notifications with HMAC-SHA256 signatures for payment events.</li>
					<li>Provide hosted checkout pages and QR codes for customer-facing payment flows.</li>
				</ul>
				<p class="mt-3 text-surface-400">The Service is provided on an "as available" basis. We reserve the right to modify, suspend, or discontinue any part of the Service at any time with reasonable notice.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">3. Account Registration</h2>
				<p>To use the Service, you must create an account and provide accurate, current, and complete information. You are responsible for:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>Maintaining the confidentiality of your account credentials, including API keys (live and test).</li>
					<li>All activities that occur under your account, whether authorized or not.</li>
					<li>Notifying us immediately at <a href="mailto:support@paychains.dev" class="text-brand-400 hover:text-brand-300 transition-colors">support@paychains.dev</a> if you suspect unauthorized access to your account or API keys.</li>
					<li>Ensuring that your use of the Service complies with all applicable laws and regulations in your jurisdiction.</li>
				</ul>
				<p class="mt-3 text-surface-400">We reserve the right to suspend or terminate accounts that violate these Terms or that we reasonably believe are engaged in fraudulent or illegal activity.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">4. API Usage</h2>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">4.1 API Access</h3>
				<p class="text-surface-400">Upon registration, you will receive API keys for both live and test environments. Test keys allow you to integrate and test without processing real transactions. Live keys process real payments on supported blockchain networks.</p>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">4.2 Rate Limits</h3>
				<p class="text-surface-400">API usage is subject to rate limits based on your plan tier:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Free:</span> 100 requests per minute</li>
					<li><span class="text-surface-300">Pro:</span> 1,000 requests per minute</li>
					<li><span class="text-surface-300">Enterprise:</span> 5,000 requests per minute (customizable)</li>
				</ul>
				<p class="mt-3 text-surface-400">Exceeding your rate limit will result in HTTP 429 responses. Persistent abuse of rate limits may result in temporary or permanent suspension of API access.</p>

				<h3 class="text-[16px] font-medium text-surface-200 mt-6 mb-3">4.3 API Key Security</h3>
				<p class="text-surface-400">You must keep your API keys secure and never expose them in client-side code, public repositories, or any publicly accessible location. You are solely responsible for any actions taken using your API keys. Compromised keys should be rotated immediately through the dashboard.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">5. Fees and Payments</h2>
				<p>PayChains charges transaction fees based on your plan tier:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">Free tier:</span> 1.0% per transaction</li>
					<li><span class="text-surface-300">Pro tier:</span> 0.5% per transaction</li>
					<li><span class="text-surface-300">Enterprise tier:</span> custom volume-based pricing</li>
				</ul>
				<p class="mt-3 text-surface-400">Fees are deducted automatically from each transaction before settlement. Network gas fees incurred during on-chain transactions are separate from PayChains fees and are borne by the appropriate party as determined by the transaction configuration.</p>
				<p class="mt-3 text-surface-400">We reserve the right to change our fee structure with 30 days' prior notice. Continued use of the Service after a fee change constitutes acceptance of the new fees.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">6. Prohibited Use</h2>
				<p>You agree not to use the Service for or in connection with:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>Any activity that violates applicable local, state, national, or international law or regulation.</li>
					<li>Money laundering, terrorist financing, or sanctions evasion.</li>
					<li>Processing payments for illegal goods or services, including but not limited to illegal drugs, weapons, stolen property, or counterfeit goods.</li>
					<li>Fraud, phishing, or any deceptive practices designed to obtain funds or information unlawfully.</li>
					<li>Market manipulation, wash trading, or any form of artificial transaction activity.</li>
					<li>Circumventing or attempting to circumvent rate limits, security measures, or access controls.</li>
					<li>Reverse-engineering, decompiling, or attempting to extract the source code of proprietary components of the Service.</li>
					<li>Reselling, sublicensing, or providing access to the Service to third parties without our written consent.</li>
					<li>Any activity that could damage, overburden, or impair the operation of the Service or interfere with other users' access.</li>
				</ul>
				<p class="mt-3 text-surface-400">We reserve the right to investigate and take appropriate action against anyone who, in our sole discretion, violates this section, including suspending or terminating access and reporting to law enforcement.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">7. Intellectual Property</h2>
				<p class="text-surface-400">The Service, including its design, code, documentation, APIs, trademarks, and all related intellectual property, is owned by PayChains and protected by applicable intellectual property laws. These Terms do not grant you any right, title, or interest in the Service except for the limited right to use it in accordance with these Terms.</p>
				<p class="mt-3 text-surface-400">Our open-source SDKs (JavaScript and Python) are licensed under their respective open-source licenses as specified in their repositories. Your use of these SDKs is governed by those licenses.</p>
				<p class="mt-3 text-surface-400">You retain all rights to your data, content, and applications that interact with the Service through our APIs.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">8. Limitation of Liability</h2>
				<p class="text-surface-400">TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li>THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS, IMPLIED, OR STATUTORY, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.</li>
					<li>PAYCHAINS SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, REVENUE, DATA, OR BUSINESS OPPORTUNITIES, ARISING FROM YOUR USE OF THE SERVICE.</li>
					<li>PAYCHAINS SHALL NOT BE LIABLE FOR LOSSES ARISING FROM BLOCKCHAIN NETWORK CONGESTION, FAILED TRANSACTIONS, SMART CONTRACT VULNERABILITIES, TOKEN PRICE VOLATILITY, BRIDGE EXPLOITS, OR OTHER RISKS INHERENT TO BLOCKCHAIN TECHNOLOGY.</li>
					<li>OUR TOTAL AGGREGATE LIABILITY FOR ALL CLAIMS ARISING FROM OR RELATED TO THE SERVICE SHALL NOT EXCEED THE TOTAL FEES PAID BY YOU TO PAYCHAINS IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.</li>
				</ul>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">9. Indemnification</h2>
				<p class="text-surface-400">You agree to indemnify, defend, and hold harmless PayChains and its officers, directors, employees, and agents from and against any claims, liabilities, damages, losses, and expenses (including reasonable attorneys' fees) arising out of or relating to your use of the Service, your violation of these Terms, or your violation of any applicable laws or third-party rights.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">10. Termination</h2>
				<p class="text-surface-400">Either party may terminate this agreement at any time:</p>
				<ul class="list-disc pl-6 space-y-2 mt-3 text-surface-400">
					<li><span class="text-surface-300">By you:</span> you may close your account at any time through the dashboard or by contacting support. Any pending transactions will be processed before account closure.</li>
					<li><span class="text-surface-300">By PayChains:</span> we may suspend or terminate your account immediately if you violate these Terms, or with 30 days' notice for any other reason.</li>
				</ul>
				<p class="mt-3 text-surface-400">Upon termination, your right to use the Service ceases immediately. We will make your transaction data available for export for 30 days following termination. Provisions that by their nature should survive termination (including Limitation of Liability, Indemnification, and Governing Law) will remain in effect.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">11. Governing Law and Dispute Resolution</h2>
				<p class="text-surface-400">These Terms shall be governed by and construed in accordance with the laws of the State of Delaware, United States, without regard to conflict of law principles. Any disputes arising from or relating to these Terms or the Service shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association, conducted in English. The arbitration shall take place in Wilmington, Delaware, or remotely at the parties' mutual agreement.</p>
				<p class="mt-3 text-surface-400">Notwithstanding the above, either party may seek injunctive or equitable relief in any court of competent jurisdiction to protect its intellectual property rights or confidential information.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">12. Changes to These Terms</h2>
				<p class="text-surface-400">We may update these Terms from time to time. We will notify you of material changes by posting the updated Terms on this page and updating the "Last updated" date. For significant changes, we will provide additional notice via email to the address associated with your account. Your continued use of the Service after any changes constitutes acceptance of the revised Terms.</p>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">13. General Provisions</h2>
				<ul class="list-disc pl-6 space-y-2 text-surface-400">
					<li><span class="text-surface-300">Entire Agreement:</span> these Terms, together with our <a href="/privacy" class="text-brand-400 hover:text-brand-300 transition-colors">Privacy Policy</a>, constitute the entire agreement between you and PayChains regarding the Service.</li>
					<li><span class="text-surface-300">Severability:</span> if any provision of these Terms is found to be unenforceable, the remaining provisions shall continue in full force and effect.</li>
					<li><span class="text-surface-300">Waiver:</span> our failure to enforce any right or provision of these Terms shall not constitute a waiver of that right or provision.</li>
					<li><span class="text-surface-300">Assignment:</span> you may not assign or transfer your rights under these Terms without our prior written consent. We may assign our rights and obligations without restriction.</li>
				</ul>
			</section>

			<section>
				<h2 class="text-xl font-semibold text-white mb-4">14. Contact Us</h2>
				<p class="text-surface-400">If you have any questions about these Terms, please contact us at:</p>
				<div class="mt-4 p-5 rounded-xl border border-white/[0.06] bg-white/[0.02]">
					<p class="text-white font-medium">PayChains</p>
					<p class="text-surface-400 mt-1">Email: <a href="mailto:support@paychains.dev" class="text-brand-400 hover:text-brand-300 transition-colors">support@paychains.dev</a></p>
				</div>
			</section>

			<div class="pt-8 border-t border-white/[0.06] text-[13px] text-surface-500">
				<p>See also our <a href="/privacy" class="text-brand-400 hover:text-brand-300 transition-colors">Privacy Policy</a>.</p>
			</div>
		</div>
	</main>
</div>
