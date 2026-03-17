import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	compilerOptions: {
		warningFilter: (warning) => {
			if (warning.code === 'a11y_label_has_associated_control') return false;
			return true;
		}
	},
	kit: {
		adapter: adapter()
	}
};

export default config;
