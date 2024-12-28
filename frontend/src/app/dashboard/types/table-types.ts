// This file contains shared TypeScript types for all table components
// Define your common table interfaces and types here
// Examples: TableColumn, SortingState, PaginationState, etc.


// Common interfaces and types for table components


// Example data types for different tables
export interface TransactionData {
  id: string;
  date: string;
  description: string;
  amount: number;
  type: string;
  categories: string[];
}

export interface CategoryData {
  id: string;
  name: string;
  budget: number;
  spent: number;
}

// Table state types
export type SortingState = {
  id: string;
  desc: boolean;
}

export type PaginationState = {
  pageIndex: number;
  pageSize: number;
}
