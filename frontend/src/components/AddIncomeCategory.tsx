"use client";

import React, { useState } from 'react'
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter,
    DialogDescription,
  } from "@/components/ui/dialog"
import { Button } from './ui/button';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { categoryService, CreateCategoryData } from '@/services/categoryService';
import { useSession } from 'next-auth/react';
import { useToast } from '@/hooks/use-toast';

const AddExpenseCategory = () => {

    const [open, setOpen]   = useState(false)
    const { data: session } = useSession()
    const [categoryName, setCategoryName] = useState('');
    const { toast } = useToast();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const createCategoryData: CreateCategoryData = {
            type: 'income' as const,
            name: categoryName
        }

        try {
            if (!session?.user?.id) {
              throw new Error('Authentication required');
            }
          
            const response = await categoryService.createCustomCategory(
              session.user.id, 
              createCategoryData
            );
          
            // Handle successful response
            if (!response) {
              toast({
                title: "Error",
                description: "Failed to create category",
              });
              return
            }else{
              setOpen(false)
              setCategoryName('')
              toast({
                title: "Success",
                description: "Category created successfully",
              })
            }


          } catch (error) {
            // Handle errors appropriately
            if (error instanceof Error) {
              console.error('Failed to create category:', error.message);
            }
            toast({
                title: "Error",
                description: "Failed to create transaction",
              });
              return
          }

    }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
            <Button>Add Income Category</Button>
        </DialogTrigger>
        <DialogContent>
            <DialogHeader>
            <DialogTitle>Add Income Category</DialogTitle>
            </DialogHeader>
            <DialogDescription></DialogDescription>
            <form onSubmit={handleSubmit}>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                        Category Name
                        </Label>
                        <Input
                            type="text" 
                            id="name" 
                            placeholder='Enter category name'
                            value={categoryName} 
                            onChange={(e) => setCategoryName(e.target.value)}  
                            className="col-span-3" 
                            required
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button type="submit">Save</Button>
                </DialogFooter>
            </form>
            
            
        </DialogContent>
    </Dialog>

  )
}

export default AddExpenseCategory