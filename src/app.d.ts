// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export type TerminalCardType = 'stock' | 'budget' | 'table'; //16


// ---------------------------------------
export interface TableColumn {
    key: string;
    label: string;
    type: 'text' | 'year' | 'integer' | 'float' | 'money' | 'ratio' | 'percentage' | 'trend-icon';
}

export interface TableData {
    [key: string]: any;
}

export {};