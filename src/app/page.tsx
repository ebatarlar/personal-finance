import { LoginForm } from "@/components/login/login-form"
import { auth } from "../../auth";
import { redirect } from "next/navigation";

export default async function Home() {

  const session = await auth();
  
  if (session) {
    redirect("/dashboard");
  }
  

  return (
    <div className="flex flex-col h-screen w-full items-center justify-center gap-4 px-4 dark md:flex-row md:justify-between">
  <div className="md:m-auto">
    <h1 className="text-center text-3xl font-bold">Welcome to Personal Finance App</h1>
  </div>
  <div className="md:m-auto">
    <LoginForm />
  </div>
</div>
  );
}
