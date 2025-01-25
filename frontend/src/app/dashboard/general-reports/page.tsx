import React from 'react'
import { DataTable } from './components/data-table'
import { columns } from './components/columns'
import { auth } from '@/auth';
import { transactionService } from '@/services/transactionService';



export default async function GeneralReportsPage() {
    // Example data - replace this with your actual data fetching logic
    const session      = await auth();
    const transactions = await transactionService.getTransactions(session?.user?.id!);
  console.log(transactions);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">General Reports</h1>
            <DataTable columns={columns} data={transactions} />
        </div>
    )
}
