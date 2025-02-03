import axios from 'axios';

const apiUrl = 'https://coral-app-c58z6.ondigitalocean.app/'


export interface Row {
    id: number
    summary: string
    call_result: string
    call_duration: string
    contact_id: number
    call_date: string
    first_name: string
    last_name: string
    phone: string
    company_name: string
  }

export interface DateRange {
    from: string;
    to: string;
}

export async function getRows(DateRange: DateRange, showResolved: boolean, showUnresolved: boolean): Promise<Row[]>{

    if(DateRange.from == '' || DateRange.to == ''){
        console.log('Date range is empty');
        DateRange.to = new Date().toLocaleDateString();
        DateRange.from = new Date(new Date().setDate(new Date().getDate() - 7)).toLocaleDateString();
        console.log(`From: ${DateRange.from}, To: ${DateRange.to}`);
    }
    
    const fromTimestamp = new Date(DateRange.from.split('/').reverse().join('-')).getTime() / 1000;
    const toTimestamp = new Date(DateRange.to.split('/').reverse().join('-')).getTime() / 1000+86400;
    console.log(`From: ${fromTimestamp}, To: ${toTimestamp}`);
    

    try {
        const response = await axios.get(apiUrl + 'callsummaries/', {
            params: {
                start_date: fromTimestamp,
                end_date: toTimestamp,
                filterResolved: showResolved,
                filterUnresolved: showUnresolved,
            },
        });
        const toReturn: Row[] = response.data.map((item: Row) => ({
            id: item.id,
            summary: item.summary,
            call_result: item.call_result,
            call_duration: item.call_duration,
            contact_id: item.contact_id,
            call_date: item.call_date,
            first_name: item.first_name,
            last_name: item.last_name,
            phone: item.phone,
            company_name: item.company_name,
        }));
        console.log('Data fetched: ', toReturn);
        return toReturn;
    }
    catch(error){
        console.error('Error fetching data: ', error);
        throw error;
    }
}
