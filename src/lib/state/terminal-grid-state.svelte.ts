import { getContext, setContext } from "svelte";

export class TerminalGridState {
    gridCols = $state<number>(1);
    gridRows = $state<number>(2);

    // ------------
    minRows = 1;
    maxRows = 4;
    // ------------
    minCols = 1;
    maxCols = 4;
    // ------------

    // need to get grid size form local storage
    constructor() {}

    setGridCols(cols: number) {
        this.gridCols = cols < 1 ? 1 : cols;
    }   

    setGridRows(rows: number) {
        this.gridRows = rows < 1 ? 1 : rows;
    }
}

const TERMINAL_GRID_KEY = Symbol('terminal-grid-state');

export const setTerminalGridState = () => {
    return setContext(TERMINAL_GRID_KEY, new TerminalGridState());
}

export const getTerminalGridState = () => {
    return getContext<ReturnType<typeof setTerminalGridState>>(TERMINAL_GRID_KEY);
}
