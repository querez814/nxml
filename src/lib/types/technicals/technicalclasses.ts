import type { MasterResponse, DailyAnalysis } from './technicalinterfaces';

export class TechnicalsTypeGuard {
	private isMasterResponse(data: unknown): data is MasterResponse {
		return (
			typeof data === 'object' &&
			data !== null &&
			'status' in data &&
			'data' in data &&
			typeof (data as MasterResponse).status === 'string'
		);
	}

	public deserializeStockData(jsonData: string): MasterResponse {
		try {
			const parsedData = JSON.parse(jsonData);

			if (!this.isMasterResponse(parsedData)) {
				throw new Error('Invalid data format');
			}

			return parsedData;
		} catch (error) {
			throw new Error(`Failed to parse stock data`);
		}
	}
	public getDailyAnalysis(data: MasterResponse, date: string): DailyAnalysis | null {
		return data.data.analysis[date] || null;
	}

	public getAvailableDates(data: MasterResponse): string[] {
		return Object.keys(data.data.analysis).sort();
	}

	public getLatestAnalysis(data: MasterResponse): DailyAnalysis | null {
		const dates = this.getAvailableDates(data);
		return dates.length > 0 ? data.data.analysis[dates[dates.length - 1]] : null;
	}
}
