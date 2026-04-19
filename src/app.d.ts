// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}

		/** Server-only env (set in cloud / ``.env`` — not ``PUBLIC_*``). */
		interface PrivateEnv {
			APP_GATE_PASS?: string;
			/** @deprecated use ``APP_GATE_PASS`` */
			APP_GATE_PASSWORD?: string;
		}
	}
}

export {};
