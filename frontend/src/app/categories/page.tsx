import { auth } from "../../../auth"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { categoryService } from "@/services/categoryService";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import AddExpenseCategory from "@/components/AddExpenseCategory";
import AddIncomeCategory from "@/components/AddIncomeCategory";







export default async function CategoriesPage() {

  const session = await auth();

  const allCategories = await categoryService.getAllCategories(session?.user?.id!);

  
  return (
    <div className="w-full">
      <Tabs defaultValue="expense" className="w-full">
        <TabsList className="flex justify-center">
          <TabsTrigger value="expense" className="flex-1 text-center">Expense</TabsTrigger>
          <TabsTrigger value="income" className="flex-1 text-center">Income</TabsTrigger>
        </TabsList>
        <TabsContent value="expense">
          <Card>
            <CardHeader>
              <CardTitle>Expense Categories Management</CardTitle>
              <CardDescription>Manage your expense categories</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {allCategories.filter(category => category.type === 'expense').map((category, index) => (
                <div 
                  key={index} 
                  className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/60 cursor-pointer"
                >
                  <div className="flex items-center gap-3">

                    <span className="font-medium">{category.name}</span>
                    {category.is_default && (
                      <Badge variant="secondary" className="text-xs">
                        Default
                      </Badge>
                    )}
                    </div>
                    <Button size="sm" variant="destructive" className="border rounded-lg bg-background">
                      Delete
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter>
              <AddExpenseCategory />  
            </CardFooter>
          </Card>
        </TabsContent>
        <TabsContent value="income">
        <Card>
            <CardHeader>
              <CardTitle>Income Categories Management</CardTitle>
              <CardDescription>Manage your income categories</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {allCategories.filter(category => category.type === 'income').map((category, index) => (
                <div 
                  key={index} 
                  className="flex items-center justify-between p-4 rounded-lg hover:bg-muted/60 cursor-pointer"
                >
                  <div className="flex items-center gap-3">

                    <span className="font-medium">{category.name}</span>
                    {category.is_default && (
                      <Badge variant="secondary" className="text-xs">
                        Default
                      </Badge>
                    )}
                    </div>
                    <Button size="sm" variant="destructive" className="border rounded-lg bg-background">
                      Delete
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter>
              <AddIncomeCategory />  
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>

    </div>
  );
}
