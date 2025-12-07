import requests
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def mostrar_banner():
    banner = f"""{Fore.RED}
▐▄• ▄  ▄▄▄·      .▄▄ · ▄▄▄ .·▄▄▄▄       ▄▄▄·  ▄▄▄·▪  
 █▌█▌▪▐█ ▄█▪     ▐█ ▀. ▀▄.▀·██▪ ██     ▐█ ▀█ ▐█ ▄███ 
 ·██·  ██▀· ▄█▀▄ ▄▀▀▀█▄▐▀▀▪▄▐█· ▐█▌    ▄█▀▀█  ██▀·▐█·
▪▐█·█▌▐█▪·•▐█▌.▐▌▐█▄▪▐█▐█▄▄▌██. ██     ▐█ ▪▐▌▐█▪·•▐█▌
•▀▀ ▀▀.▀    ▀█▄▀▪ ▀▀▀▀  ▀▀▀ ▀▀▀▀▀•      ▀  ▀ .▀   ▀▀▀
     
                                            ▐▌  
{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}================ Data Breach Lookup ================ \n{Style.RESET_ALL}"""
    print(banner)
    
    spaces = 22
    print(f"{' ' * spaces}{Fore.WHITE}{Style.BRIGHT}By: @Oxvileness\n{Style.RESET_ALL}")

def consultar_email_breach(email):
    api_url = f'https://api.xposedornot.com/v1/breach-analytics?email={email}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        mostrar_resultados(data)

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✖ Error connecting to the API: {e}")

def mostrar_resultados(data):
    print(f"\n{Fore.CYAN} QUERY RESULTS{Style.RESET_ALL}")
    
    # Show Risk Summary
    risk_info = data.get("BreachMetrics", {}).get("risk", [{}])[0]
    print(f"\n{Fore.YELLOW} Risk level: {Fore.RED if risk_info.get('risk_label') == 'High' else Fore.YELLOW if risk_info.get('risk_label') == 'Medium' else Fore.GREEN}{risk_info.get('risk_label', 'Desconocido')} ({risk_info.get('risk_score', '?')}/100)")
    
    # Show Breach Summary
    breaches_summary = data.get("BreachesSummary", {}).get("site", "").split(";")
    if breaches_summary and breaches_summary[0]:
        print(f"\n{Fore.YELLOW} Breaches Found: {Fore.WHITE}{len(breaches_summary)}")
        print(f"{Fore.YELLOW} Affected Sites: {Fore.WHITE}{', '.join(breaches_summary)}")
    else:
        print(f"\n{Fore.GREEN} No known breaches were found on this email")
    
    # Show metrics by industry
    industry_metrics = data.get("BreachMetrics", {}).get("industry", [[]])[0]
    if industry_metrics:
        print(f"\n{Fore.YELLOW}  Breaches By Industry:")
        for industry in industry_metrics:
            if isinstance(industry, list) and len(industry) == 2 and industry[1] > 0:
                print(f"  {Fore.CYAN}{industry[0]}: {Fore.WHITE}{industry[1]} brecha(s)")
    
    # Show password details
    password_strength = data.get("BreachMetrics", {}).get("passwords_strength", [{}])[0]
    if password_strength:
        print(f"\n{Fore.YELLOW} Status Of Exposed Passwords:")
        print(f"  {Fore.RED}Easy to crack: {password_strength.get('EasyToCrack', 0)}")
        print(f"  {Fore.YELLOW}Plain text: {password_strength.get('PlainText', 0)}")
        print(f"  {Fore.GREEN}Hash strong: {password_strength.get('StrongHash', 0)}")
        print(f"  {Fore.BLUE}Unknown: {password_strength.get('Unknown', 0)}")
    
    # Show Breach Details
    exposed_breaches = data.get("ExposedBreaches", {}).get("breaches_details", [])
    if exposed_breaches:
        print(f"\n{Fore.YELLOW} BREACH DETAILS:{Style.RESET_ALL}")
        for breach in exposed_breaches:
            print(f"\n{Fore.MAGENTA}➤ {breach.get('breach', 'Desconocido')} ({breach.get('industry', '?')})")
            print(f"  {Fore.CYAN} Year: {breach.get('xposed_date', '?')}")
            print(f"  {Fore.CYAN} Records Affected: {breach.get('xposed_records', '?')}")
            print(f"  {Fore.CYAN} Data Exposed: {breach.get('xposed_data', '?')}")
            print(f"  {Fore.CYAN} Reference: {breach.get('references', '?')}")
            print(f"  {Fore.CYAN} Details: {breach.get('details', '?')[:1000]}...")

if __name__ == "__main__":
    mostrar_banner()
    print(f"{Fore.CYAN} Email security breach verification")
    email = input(f"{Fore.WHITE}Enter your Email Address: ")
    consultar_email_breach(email)
