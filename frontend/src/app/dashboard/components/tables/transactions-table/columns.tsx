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
    accessorKey: 'categories',
    header: 'Categories',
    cell: ({ row }) => {
      const categories = row.getValue('categories') as string[]
      return (
        <div className="flex flex-wrap gap-1">
          {categories.map((category, index) => (
            <span 
              key={index} 
              className="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-secondary"
            >
              {category}
            </span>
          ))}
        </div>
      )
    }
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
