import json
import google.generativeai as genai
from config import Config

GEMINI_MODEL = 'gemini-3.5-flash-lite'

class GeminiService:
    _configured = False

    @classmethod
    def _initialize_gemini(cls):
        if cls._configured:
            return True
        
        api_key = Config.GEMINI_API_KEY
        if api_key:
            try:
                genai.configure(api_key=api_key)
                cls._configured = True
                return True
            except Exception as e:
                print(f"Failed to configure Gemini API: {e}")
        return False

    @staticmethod
    def get_product_summary(product_name, specifications, description):
        """Generates a premium summary of a product using Gemini or a fallback heuristic."""
        if GeminiService._initialize_gemini():
            try:
                model = genai.GenerativeModel(GEMINI_MODEL)
                prompt = (
                    f"You are a professional tech and product reviewer. Summarize the following product in a premium, engaging way:\n"
                    f"Name: {product_name}\n"
                    f"Specs: {specifications}\n"
                    f"Description: {description}\n"
                    f"Provide a 3-sentence summary highlighting why it stands out."
                )
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini summary API failed, using fallback: {e}")
        
        # Fallback Heuristics
        if "iPhone" in product_name:
            return f"The {product_name} represents a peak refinement of the modern smartphone. With its hardware-software synergy, stellar optics, and efficient engine, it offers a seamless and dependable experience for creators and everyday users alike."
        elif "Galaxy" in product_name:
            return f"The {product_name} pushes the boundaries of Android capabilities, boasting a brilliant display, robust multi-tasking processor, and a highly versatile camera suite that satisfies both power-users and productivity enthusiasts."
        elif "MacBook" in product_name:
            return f"The {product_name} defines portability and raw efficiency. Built around Apple Silicon, it delivers extraordinary battery life and near-silent operation in an ultra-sleek, premium chassis that handles everyday and creative workloads easily."
        
        return f"The {product_name} is a stellar product combining premium design, solid performance, and impressive feature integration. It offers great value and satisfies the demands of both hobbyists and daily users."

    @staticmethod
    def get_pros_and_cons(product_name, specifications):
        """Generates 3 pros and 3 cons in JSON format using Gemini or a fallback heuristic."""
        default_fallback = {
            "pros": [
                "Premium design and exceptional build quality",
                "Stellar display visibility and high color accuracy",
                "Strong performance and power-efficient battery management"
            ],
            "cons": [
                "Premium pricing and lack of charger in the box",
                "Slightly slower charging speed compared to competitors",
                "Storage upgrades can be expensive"
            ]
        }

        if GeminiService._initialize_gemini():
            try:
                model = genai.GenerativeModel(GEMINI_MODEL)
                prompt = (
                    f"Analyze this product and list exactly 3 pros and 3 cons. Format the output strictly as a JSON object with keys 'pros' and 'cons', where each key contains a list of 3 strings. Do not include markdown formatting.\n"
                    f"Product: {product_name}\n"
                    f"Specs: {specifications}"
                )
                response = model.generate_content(prompt)
                text = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(text)
            except Exception as e:
                print(f"Gemini pros/cons API failed, using fallback: {e}")

        # Specific custom fallback logic to feel personalized and real
        if "iPhone 15" in product_name:
            return {
                "pros": [
                    "Dynamic Island integration for active alerts",
                    "New 48MP main camera captures rich details",
                    "A16 Bionic delivers snappy, lag-free performance"
                ],
                "cons": [
                    "USB-C is restricted to USB 2.0 speeds",
                    "Matches last year's 60Hz display refresh rate",
                    "Noticeable thermal throttling during long gaming sessions"
                ]
            }
        elif "Galaxy S24" in product_name:
            return {
                "pros": [
                    "Industry-best Dynamic AMOLED 2X flat display",
                    "Long-term 7 years of OS upgrade path",
                    "Advanced Galaxy AI intelligence features preloaded"
                ],
                "cons": [
                    "Baseline 128GB version uses slower UFS 3.1 storage",
                    "Camera processing sometimes over-saturates skin tones",
                    "Minimal model charging speeds capped at 25W"
                ]
            }
        elif "MacBook Air" in product_name:
            return {
                "pros": [
                    "Fanless silent design remains perfectly quiet",
                    "Thin, light, and robust aluminum unibody",
                    "M2 chip provides incredible price-to-performance"
                ],
                "cons": [
                    "Base model only supports one external display",
                    "8GB base RAM can struggle under heavy multitasking",
                    "SSD speeds are slower on the 256GB baseline"
                ]
            }

        return default_fallback

    @staticmethod
    def get_comparison_verdict(products_list):
        """Generates an AI assessment and comparison summary for up to 4 products."""
        names = [p.name for p in products_list]
        details = [{
            "name": p.name,
            "category": p.category,
            "specs": p.specifications
        } for p in products_list]

        if GeminiService._initialize_gemini():
            try:
                model = genai.GenerativeModel(GEMINI_MODEL)
                prompt = (
                    f"Write a comparison verdict for these products: {json.dumps(names)}.\n"
                    f"Here are their specs: {json.dumps(details)}.\n"
                    f"Summarize the differences in 3 sentences, explicitly note which represents the 'Best overall value for money', "
                    f"which has the 'Best hardware features', and provide a final recommendation."
                )
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini comparison API failed, using fallback: {e}")

        # High fidelity fallback matrix comparison logic
        if any("iPhone 15" in name for name in names) and any("Galaxy S24" in name for name in names):
            return (
                "If you want the best camera precision and a mature, seamless ecosystem, go for the Apple iPhone 15. "
                "For overall versatility, customization, and cutting-edge multitasking tools, the Samsung Galaxy S24 is the superior value. "
                "For gamers or performance seekers on a tighter budget, the OnePlus 12R stands out as the ultimate value champion."
            )
        
        # General comparison
        p_list_str = " vs ".join(names)
        return (
            f"Comparing {p_list_str} reveals a tight trade-off. The highest-priced option provides premium craftsmanship "
            f"and class-leading performance. However, for buyers looking to maximize utility relative to budget, the "
            f"mid-tier options in this comparison list offer 90% of the functional value at a fraction of the cost."
        )

    @staticmethod
    def get_recommendation_advice(budget, category, usage, battery_preference):
        """Returns personalized recommendation advice based on user filters."""
        if GeminiService._initialize_gemini():
            try:
                model = genai.GenerativeModel(GEMINI_MODEL)
                prompt = (
                    f"A user wants an AI product recommendation.\n"
                    f"Category: {category}\n"
                    f"Budget: {budget}\n"
                    f"Usage target: {usage} (e.g. Gaming, Student, Photography)\n"
                    f"Battery priorities: {battery_preference}\n"
                    f"Write a short, engaging recommendation analysis, helping them understand what they should buy. Limit it to 3 sentences."
                )
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                print(f"Gemini recommendation API failed, using fallback: {e}")

        # Intelligent Fallback
        advice = f"Based on your preference for {usage} and a budget under {budget}, we recommend looking at mid-tier options. "
        if category == "Mobiles":
            if float(budget) < 40000:
                advice += "The OnePlus 12R is your best choice, offering a flagship Snapdragon 8 Gen 2 CPU and a massive 5500 mAh battery."
            elif float(budget) < 70000:
                advice += "The Samsung Galaxy S24 fits perfectly, providing advanced AI features, a high-quality AMOLED screen, and long-term OS support."
            else:
                advice += "The iPhone 15 (128GB) is our top pick. Its combination of an A16 processor and superb 48MP main camera makes it an ideal driver."
        elif category == "Laptops":
            advice += "The MacBook Air M2 (256GB) offers unmatched portability, silent fanless runtimes, and battery endurance perfect for day-long study sessions."
        else:
            advice += "Sony WH-1000XM5 wireless NC headphones fit this tier excellently, delivering top-rated active noise canceling and battery life."

        return advice
