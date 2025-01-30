import type { Stock } from '../../lib/types/types';

const api_url = import.meta.env.VITE_API_URL;
async function fetchStocks(endpoint: string): Promise<Stock[]> {
	const response = await fetch(`${api_url}${endpoint}`);
	if (!response.ok) throw new Error(`Failed to fetch stocks from ${endpoint}`);
	return response.json();
}

export async function fetchStocksBySector(): Promise<Record<string, Stock[]>> {
	const response = await fetch(`${api_url}/stocks/by-sector`);
	if (!response.ok) throw new Error('Failed to fetch stocks by sector');
	return response.json();
}

export const stockApi = {
	fetchSoftwareInfra: () => fetchStocks('/swinfra'),
	fetchSoftwareApp: () => fetchStocks('/swapp'),
	fetchCommunicationEquipment: () => fetchStocks('/commeqpt'),
	fetchDrugManufacturers: () => fetchStocks('/drugman'),
	fetchElectronicComponents: () => fetchStocks('/eleccomponents'),
	fetchSemiconductors: () => fetchStocks('/semi'),
	fetchSemiconductorEquipment: () => fetchStocks('/semi-eqpt'),
	fetchSciTechEquipment: () => fetchStocks('/sci-eqpt'),
	fetchElectricalEquipment: () => fetchStocks('/elec-eqpt'),
	fetchTelecom: () => fetchStocks('/telecom'),
	fetchRestaurants: () => fetchStocks('/restaraunt'),
	fetchSpecialtyChemicals: () => fetchStocks('/specchem'),
	fetchSolar: () => fetchStocks('/solar'),
	fetchEntertainment: () => fetchStocks('/entertainment'),
	fetchMachinery: () => fetchStocks('/machinery'),
	fetchInternetContent: () => fetchStocks('/internetcontent'),
	fetchIT: () => fetchStocks('/it')
};

export const industryOptions = [
	{
		value: 'software-infra',
		label: 'Software - Infrastructure',
		fetch: stockApi.fetchSoftwareInfra
	},
	{ value: 'software-app', label: 'Software - Application', fetch: stockApi.fetchSoftwareApp },
	{
		value: 'comm-equipment',
		label: 'Communication Equipment',
		fetch: stockApi.fetchCommunicationEquipment
	},
	{
		value: 'drug-manufacturers',
		label: 'Drug Manufacturers',
		fetch: stockApi.fetchDrugManufacturers
	},
	{
		value: 'electronic-components',
		label: 'Electronic Components',
		fetch: stockApi.fetchElectronicComponents
	},
	{ value: 'semiconductors', label: 'Semiconductors', fetch: stockApi.fetchSemiconductors },
	{
		value: 'semiconductor-equipment',
		label: 'Semiconductor Equipment',
		fetch: stockApi.fetchSemiconductorEquipment
	},
	{
		value: 'scitech-equipment',
		label: 'Scientific & Technical Instruments',
		fetch: stockApi.fetchSciTechEquipment
	},
	{
		value: 'electrical-equipment',
		label: 'Electrical Equipment',
		fetch: stockApi.fetchElectricalEquipment
	},
	{ value: 'telecom', label: 'Telecom Services', fetch: stockApi.fetchTelecom },
	{ value: 'restaurants', label: 'Restaurants', fetch: stockApi.fetchRestaurants },
	{
		value: 'specialty-chemicals',
		label: 'Specialty Chemicals',
		fetch: stockApi.fetchSpecialtyChemicals
	},
	{ value: 'solar', label: 'Solar', fetch: stockApi.fetchSolar },
	{ value: 'entertainment', label: 'Entertainment', fetch: stockApi.fetchEntertainment },
	{ value: 'machinery', label: 'Specialty Industrial Machinery', fetch: stockApi.fetchMachinery },
	{
		value: 'internet-content',
		label: 'Internet Content & Information',
		fetch: stockApi.fetchInternetContent
	},
	{ value: 'it-services', label: 'IT Services', fetch: stockApi.fetchIT }
];

export async function screenStocks(params: {
	min_market_cap?: number;
	max_pe_ratio?: number;
	sectors?: string[];
	min_change_1m?: number;
	max_change_1m?: number;
}): Promise<Stock[]> {
	const queryParams = new URLSearchParams();

	Object.entries(params).forEach(([key, value]) => {
		if (value !== undefined && value !== null) {
			if (Array.isArray(value)) {
				value.forEach((v) => queryParams.append(key, v));
			} else {
				queryParams.append(key, value.toString());
			}
		}
	});

	return fetchStocks(`/stocks/screen?${queryParams}`);
}
