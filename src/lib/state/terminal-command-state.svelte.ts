import { getContext, setContext } from "svelte";

export class TerminalCommandState {
    executedCommands = $state<Array<string>>(new Array());
    pendingCommand = $state<string>('');
    currentHistoryIndex = $state<number>(0);

    isDisabled = $state<boolean>(false);


    constructor() {}

    setPendingCommand(command: string) { this.pendingCommand = command; }

    clearPendingCommand() { this.pendingCommand = ''; }

    executeCommand() {
        // NOTE: Do some logic here
           // parse command
            // execute command
        // ------------------------

        
        this.executedCommands.unshift(this.pendingCommand);
        // NOTE: Do some logic here
        console.log(this.executedCommands);
        //alert(this.pendingCommand);
        // ------------------------
        this.clearPendingCommand();
        this.currentHistoryIndex = -1;
    }

    clearExecutedCommands() {
        this.executedCommands  = new Array();
    }

    getExecutedCommandCount() {
        return this.executedCommands.length;
    }

    navigateHistory(direction: 'up' | 'down') {
        if (direction === 'up') {
            if (this.currentHistoryIndex === this.executedCommands.length - 1) {
                return;
            }

            this.currentHistoryIndex++;
        } else {
            if (this.currentHistoryIndex === -1) {
                this.setPendingCommand(this.pendingCommand);
                return;
            }

            this.currentHistoryIndex--;

            if (this.currentHistoryIndex === -1) {
                this.clearPendingCommand();
            }
        }

        if ( this.currentHistoryIndex >= 0 && this.currentHistoryIndex < this.executedCommands.length) { 
            this.setPendingCommand(this.executedCommands[this.currentHistoryIndex]);
        }
    }
}

const TERMINAL_COMMAND_KEY = Symbol('terminal-grid-state');

export const setTerminalCommandState = () => {
    return setContext(TERMINAL_COMMAND_KEY, new TerminalCommandState());
}

export const getTerminalCommandState = () => {
    return getContext<ReturnType<typeof setTerminalCommandState>>(TERMINAL_COMMAND_KEY);
}
