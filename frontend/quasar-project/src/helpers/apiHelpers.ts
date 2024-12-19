import axios from 'axios';

const apiUrl = 'https://coral-app-c58z6.ondigitalocean.app/'

export interface Row {
    id: number;
    summary: string;
    call_result: string;
    call_duration: string;
    contact_id: number;
    
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
    

    try{
        const response = await axios.get(apiUrl + 'callsummaries/', {
            params: {
                start_date: fromTimestamp,
                end_date: toTimestamp,
                filterResolved: showResolved,
                filterUnresolved: showUnresolved,
            },
          });
        console.log('Data fetched: ', response.data);
        return response.data;
    }
    catch(error){
        console.error('Error fetching data: ', error);
        throw error;
    }
}
