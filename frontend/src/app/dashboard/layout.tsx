import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { redirect } from "next/navigation"
import { auth } from "../../../auth";
import { Toaster } from "@/components/ui/toaster";
import { cookies } from "next/headers";

export default async function Layout({ children }: { children: React.ReactNode }) {
  const session = await auth();
  
  if (!session) {
    redirect("/");
  }

  const cookieStore = await cookies()
  const defaultOpen = cookieStore.get("sidebar:state")?.value === "true"


  return (
    <div className="dark h-full">
      <div className="min-h-screen bg-background">
        <SidebarProvider defaultOpen={defaultOpen}>
          <AppSidebar />
          <main className="flex-1 min-h-screen bg-background text-foreground">
            <SidebarTrigger />
            <div className="container mx-auto p-4">
              {children}
            </div>
            <Toaster />
          </main>
        </SidebarProvider>
      </div>
    </div>
  )
}