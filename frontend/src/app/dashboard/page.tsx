import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import AddTransDialog from "@/components/AddTransDialog"
import { DataTable } from "./components/tables/transactions-table/transactions-table"
import { columns } from "./components/tables/transactions-table/columns"
import { TransactionData } from "./types/table-types"
import { transactionService } from "@/services/transactionService"
import { auth } from "../../../auth"





export default async function DashboardPage() {

  const session = await auth();

  const transactions = await transactionService.getTransactions(session?.user?.id!);

  console.log(transactions);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Dashboard</h2>
        <AddTransDialog />
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Balance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$12,546.00</div>
            <p className="text-xs text-muted-foreground">+20.1% from last month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Income</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$4,935.00</div>
            <p className="text-xs text-muted-foreground">+4.3% from last month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Expenses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$2,435.00</div>
            <p className="text-xs text-muted-foreground">+10.2% from last month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Savings Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">50.7%</div>
            <p className="text-xs text-muted-foreground">+2.4% from last month</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2">


        
        <Card className="w-fit">
          <CardHeader>
            <CardTitle>Recent Transactions</CardTitle>
          </CardHeader>
          <CardContent>
          <DataTable columns={columns} data={transactions.transactions} />
          </CardContent>
        </Card>
        
        
        <Card>
          <CardHeader>
            <CardTitle>Monthly Budget Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Category</TableHead>
                  <TableHead>Spent</TableHead>
                  <TableHead>Budget</TableHead>
                  <TableHead className="text-right">Remaining</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell>Food & Groceries</TableCell>
                  <TableCell>$450.32</TableCell>
                  <TableCell>$600.00</TableCell>
                  <TableCell className="text-right text-green-600">$149.68</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Transportation</TableCell>
                  <TableCell>$245.23</TableCell>
                  <TableCell>$300.00</TableCell>
                  <TableCell className="text-right text-green-600">$54.77</TableCell>
                </TableRow>
                
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
