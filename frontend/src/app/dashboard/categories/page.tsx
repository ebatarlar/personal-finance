import { auth } from "@/auth"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { categoryService } from "@/services/categoryService";
import { CategoryCard } from "./components/CategoryCard";

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
          <CategoryCard type="expense" categories={allCategories} />
        </TabsContent>
        <TabsContent value="income">
          <CategoryCard type="income" categories={allCategories} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
