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
    accessorKey: 'type',
    header: 'Type',
    cell: ({ row }) => {
      const type = row.getValue('type') as string
      return (
        <span className={type === 'expense' ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>
          {type.charAt(0).toUpperCase() + type.slice(1)}
        </span>
      )
    }
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
    header: 'Amount',
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue("amount"))
      const formatted = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
      }).format(amount)
      return <span className="font-medium">{formatted}</span>
    }
  }
]
