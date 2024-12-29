import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { enhancedImages } from '@sveltejs/enhanced-img';

// Main Vite configuration
export default defineConfig({
	plugins: [sveltekit(), enhancedImages()],
	envPrefix: 'VITE_' // Prefix for environment variables
});
