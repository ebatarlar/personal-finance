// This file defines the columns for the transactions table
// Define your column configurations here including:
// - Column headers
// - Data accessors
// - Custom cell renderers
// - Sorting options
// - Filter configurations

'use client'

import { ColumnDef } from "@tanstack/react-table"
import { TransactionData } from '@/app/dashboard/types/table-types'

export const columns: ColumnDef<TransactionData>[] = [
  {
    accessorKey: 'date',
    header: 'Date'
  },
  {
    accessorKey: 'description',
    header: 'Description',
  },
  {
    accessorKey: 'category',
    header: 'Category',
  },
  {
    accessorKey: 'amount',
    header: 'Amount'
  }
]
