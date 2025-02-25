"use client";

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/hooks/use-toast";
import { useState, useEffect } from "react"
import { Calendar } from "./ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import { CalendarIcon } from "lucide-react";
import { format } from 'date-fns';
import { cn } from "@/lib/utils";
import { Checkbox } from "@/components/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useSession } from "next-auth/react"
import { Session } from "next-auth"
import { transactionService } from "@/services/transactionService";
import { categoryService } from "@/services/categoryService";

interface Category {
  type: 'expense' | 'income';
  name: string;
  is_default: boolean;
}

const AddTransDialog = () => {
  
  const [amount, setAmount]           = useState("")
  const [description, setDescription] = useState("")
  const [date, setDate]               = useState<Date>()
  const [open, setOpen]               = useState(false)
  const [transactionType, setTransactionType] = useState<string>("")
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const { data: session } = useSession()
  const { toast }                     = useToast()

  useEffect(() => {
    const fetchCategories = async () => {
      if (session?.user?.id) {
        try {
          const allCategories = await categoryService.getAllCategories(session.user.id);
          setCategories(allCategories);
        } catch (error) {
          console.error('Error fetching categories:', error);
          toast({
            title: "Error",
            description: "Failed to fetch categories",
          });
        }
      }
    };

    if (open) {
      fetchCategories();
    }
  }, [open, session?.user?.id]);

  const filteredCategories = categories.filter(
    category => category.type === transactionType
  );

  const handleCategoryChange = (category: string, checked: boolean) => {
    if (checked) {
      setSelectedCategories(prev => [...prev, category]);
    } else {
      setSelectedCategories(prev => prev.filter(c => c !== category));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (selectedCategories.length === 0) {
      toast({
        title: "Error",
        description: "Please select at least one category",
        variant: "destructive"
      });
      return;
    }

    const transactionData = {
      user_id: session?.user.id,
      type: transactionType,
      categories: selectedCategories,
      amount: typeof amount === 'number' ? amount : parseFloat(amount),
      date: date ? format(date, 'yyyy-MM-dd') : format(new Date(), 'yyyy-MM-dd'),
      description: description || "",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }

    const response = await transactionService.createTransaction(transactionData)

    if(!response) {
      toast({
        title: "Error",
        description: "Failed to create transaction",
      });
      return
    }else {
      // Clear form and close dialog
      setAmount("");
      setDescription("");
      setSelectedCategories([]);
      setOpen(false);
      toast({
        title: "Success",
        description: "Transaction has been created successfully",
      });
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Add Transaction</Button>
      </DialogTrigger>
      <DialogContent className="w-[90%]">
        <DialogTitle>Add New Transaction</DialogTitle>
        <DialogDescription>
          Add a new financial transaction with amount and description fields
        </DialogDescription>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="amount" className="text-right">
                Date
              </Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant={"outline"}
                    className={cn(
                      "w-[240px] justify-start text-left font-normal",
                      !date && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon />
                    {date ? format(date, "PPP") : <span>Pick a date</span>}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={setDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="amount" className="text-right">
                Type
              </Label>
              <Select 
                onValueChange={(value) => {
                  setTransactionType(value);
                  setSelectedCategories([]); // Reset categories when type changes
                }} 
                value={transactionType}
              >
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="expense">Expense</SelectItem>
                  <SelectItem value="income">Income</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="category" className="text-right">
                Categories
              </Label>
              <div className="col-span-3 flex flex-col gap-2">
                {filteredCategories.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    {transactionType 
                      ? "No categories available for this type" 
                      : "Select a transaction type to filter categories"}
                  </p>
                ) : (
                  <div className="grid grid-cols-2 gap-4">
                    {filteredCategories.map((category) => (
                      <div key={category.name} className="flex items-center space-x-2">
                        <Checkbox 
                          id={category.name}
                          checked={selectedCategories.includes(category.name)}
                          onCheckedChange={(checked) => 
                            handleCategoryChange(category.name, checked as boolean)
                          }
                          disabled={!transactionType}
                        />
                        <label
                          htmlFor={category.name}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                        >
                          {category.name}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
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