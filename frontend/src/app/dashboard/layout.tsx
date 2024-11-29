import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { redirect } from "next/navigation"
import { auth } from "../../../auth";

export default async function Layout({ children }: { children: React.ReactNode }) {
  const session = await auth();
  
  if (!session) {
    redirect("/");
  }

  return (
    <div className="dark h-full">
      <div className="min-h-screen bg-background">
        <SidebarProvider>
          <AppSidebar />
          <main className="min-h-screen bg-background text-foreground">
            <SidebarTrigger />
            {children}
          </main>
        </SidebarProvider>
      </div>
    </div>
  )
}
