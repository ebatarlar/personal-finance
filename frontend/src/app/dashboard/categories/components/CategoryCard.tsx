'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CategoryList } from "./CategoryList";
import AddExpenseCategory from "@/components/AddExpenseCategory";
import AddIncomeCategory from "@/components/AddIncomeCategory";

interface Category {
  name: string;
  type: 'income' | 'expense';
  is_default: boolean;
}

interface CategoryCardProps {
  type: 'income' | 'expense';
  categories: Category[];
}

export function CategoryCard({ type, categories }: CategoryCardProps) {
  const filteredCategories = categories.filter(category => category.type === type);
  const title = `${type.charAt(0).toUpperCase() + type.slice(1)} Categories Management`;
  const AddComponent = type === 'income' ? AddIncomeCategory : AddExpenseCategory;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <CardDescription>Manage your {type} categories</CardDescription>
      </CardHeader>
      <CardContent>
        <CategoryList categories={filteredCategories} />
      </CardContent>
      <CardFooter>
        <AddComponent />
      </CardFooter>
    </Card>
  );
}
