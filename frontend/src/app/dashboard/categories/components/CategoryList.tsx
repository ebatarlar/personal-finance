'use client';

import { Badge } from "@/components/ui/badge";

interface Category {
  name: string;
  type: 'income' | 'expense';
  is_default: boolean;
}

interface CategoryListProps {
  categories: Category[];
}

export function CategoryList({ categories }: CategoryListProps) {
  return (
    <div className="grid gap-4">
      {categories.map((category, index) => (
        <div 
          key={index} 
          className="flex items-center p-4 rounded-lg hover:bg-muted/60"
        >
          <div className="flex items-center gap-3">
            <span className="font-medium">{category.name}</span>
            {category.is_default && (
              <Badge variant="secondary" className="text-xs">
                Default
              </Badge>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
