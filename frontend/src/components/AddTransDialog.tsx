"use client";

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast";
import { useState } from "react"

const AddTransDialog = () => {
  
  const [amount, setAmount]           = useState("")
  const [description, setDescription] = useState("")
  const [open, setOpen]               = useState(false)
  const { toast }                     = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch("http://localhost:8000/api/transactions/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          amount: parseFloat(amount),
          description,
        }),
      })

      if (response.ok) {
        // Clear form and close dialog
        setAmount("");
        setDescription("");
        setOpen(false);
        toast({
          title: "Success",
          description: "Transaction has been created successfully",
        });
      } else {
        console.error("Failed to create transaction")
      }
    } catch (error) {
      console.error("Error creating transaction:", error)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Add Transaction</Button>
      </DialogTrigger>
      <DialogContent 
        className="w-[90%]" 
        aria-describedby="dialog-description"
      >
        <DialogHeader>
          <DialogTitle>Add New Transaction</DialogTitle>
        </DialogHeader>
        <div id="dialog-description" className="sr-only">
          Form to add a new financial transaction with amount and description fields
        </div>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="amount" className="text-right">
                Amount
              </Label>
              <Input
                id="amount"
                type="number"
                className="col-span-3"
                placeholder="Enter amount"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="description" className="text-right">
                Description
              </Label>
              <Input
                id="description"
                className="col-span-3"
                placeholder="Enter description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="flex justify-end">
            <Button type="submit">Save Transaction</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default AddTransDialog