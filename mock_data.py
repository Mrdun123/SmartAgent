"""
迪拜商场互动服务 Agent - Mock Data & Tools
用于演示 Agent 功能的模拟数据和工具函数
"""

# ==================== 模拟数据库 ====================

# 店铺信息数据库
SHOPS = {
    "Hermès": {
        "name": "Hermès",
        "floor": "Ground Floor",
        "category": "Luxury Fashion",
        "description": "法国顶级奢侈品牌，提供手袋、丝巾、配饰等经典产品。",
        "location": "Ground Floor, Zone A, near Main Entrance"
    },
    "Louis Vuitton": {
        "name": "Louis Vuitton",
        "floor": "Ground Floor",
        "category": "Luxury Fashion",
        "description": "世界知名奢侈品牌，专营皮具、箱包及时尚配饰。",
        "location": "Ground Floor, Zone B, opposite Fountain"
    },
    "Chanel": {
        "name": "Chanel",
        "floor": "1st Floor",
        "category": "Luxury Fashion",
        "description": "经典法式奢华品牌，提供时装、香水和美妆产品。",
        "location": "1st Floor, Zone C, near Escalator 3"
    },
    "% Arabica": {
        "name": "% Arabica",
        "floor": "2nd Floor",
        "category": "Cafe & Dining",
        "description": "精品咖啡馆，提供手冲咖啡和轻食。",
        "location": "2nd Floor, Food Court Area, near Window Seating"
    },
    "Shake Shack": {
        "name": "Shake Shack",
        "floor": "2nd Floor",
        "category": "Cafe & Dining",
        "description": "美式快餐品牌，招牌汉堡和奶昔。",
        "location": "2nd Floor, Food Court, Zone D"
    },
    "Zara": {
        "name": "Zara",
        "floor": "1st Floor",
        "category": "Fashion Retail",
        "description": "西班牙快时尚品牌，提供男女装及童装。",
        "location": "1st Floor, Zone E, near Cinema Entrance"
    },
    "Apple Store": {
        "name": "Apple Store",
        "floor": "Ground Floor",
        "category": "Electronics",
        "description": "苹果官方零售店，销售 iPhone、Mac、iPad 等产品及配件。",
        "location": "Ground Floor, Zone F, Central Plaza"
    },
    "Customer Service Center": {
        "name": "Customer Service Center",
        "floor": "Ground Floor",
        "category": "Service Facility",
        "description": "商场客服中心，提供咨询、失物招领、轮椅租赁等服务。",
        "location": "Ground Floor, Main Entrance Lobby"
    },
    "Prayer Room": {
        "name": "Prayer Room",
        "floor": "3rd Floor",
        "category": "Service Facility",
        "description": "祈祷室，提供安静的礼拜空间。",
        "location": "3rd Floor, near Restrooms, Zone G"
    },
    "VIP Lounge": {
        "name": "VIP Lounge",
        "floor": "3rd Floor",
        "category": "Service Facility",
        "description": "VIP 休息室，为高级会员提供休息和饮品服务。",
        "location": "3rd Floor, Zone H, requires membership card"
    }
}

# 停车场数据库
PARKING = {
    "DXB-1234": "B2-A05",
    "DXB-5678": "B1-C12",
    "AD-9999": "B2-D08",
    "SHJ-4321": "B1-B03",
    "AUH-7890": "B2-E15"
}

# 用户状态（内存存储）
class UserState:
    """用于 Demo 的用户状态管理（支持持久化存储）"""
    def __init__(self, data_file="user_data.json"):
        self.data_file = data_file
        self.users = {}
        self.load()  # 启动时加载数据

    def load(self):
        """从JSON文件加载用户数据"""
        import json
        import os

        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
                print(f"✅ 已从 {self.data_file} 加载用户数据")
            except Exception as e:
                print(f"⚠️ 加载用户数据失败: {e}")
                self.users = {}
        else:
            print(f"📝 {self.data_file} 不存在，将创建新的用户数据")
            self.users = {}

    def save(self):
        """保存用户数据到JSON文件"""
        import json

        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            print(f"💾 用户数据已保存到 {self.data_file}")
        except Exception as e:
            print(f"⚠️ 保存用户数据失败: {e}")

    def get_user(self, user_id):
        """获取或创建用户"""
        if user_id not in self.users:
            self.users[user_id] = {
                "points": 0,
                "coupons": []
            }
            self.save()  # 新建用户时保存
        return self.users[user_id]

    def add_points(self, user_id, amount):
        """增加积分"""
        user = self.get_user(user_id)
        user["points"] += amount
        self.save()  # 积分变化时保存
        return user["points"]

    def deduct_points(self, user_id, amount):
        """扣除积分"""
        user = self.get_user(user_id)
        if user["points"] >= amount:
            user["points"] -= amount
            self.save()  # 积分变化时保存
            return True
        return False

    def add_coupon(self, user_id, coupon):
        """添加优惠券"""
        user = self.get_user(user_id)
        user["coupons"].append(coupon)
        self.save()  # 优惠券变化时保存

    def get_points(self, user_id):
        """获取当前积分"""
        return self.get_user(user_id)["points"]

    def get_coupons(self, user_id):
        """获取优惠券列表"""
        return self.get_user(user_id)["coupons"]

# 全局用户状态实例
USER_STATE = UserState()


# ==================== 工具函数 ====================

def find_parking(plate_number):
    """
    查找车辆停车位置

    Args:
        plate_number: 车牌号（如 "DXB-1234"）

    Returns:
        dict: 包含停车位信息或错误信息
    """
    print(f"DEBUG: Tool [find_parking] called with plate_number='{plate_number}'")

    if plate_number in PARKING:
        parking_spot = PARKING[plate_number]
        return {
            "success": True,
            "plate_number": plate_number,
            "parking_spot": parking_spot,
            "message": f"您的车辆 {plate_number} 停放在 {parking_spot} 区域。"
        }
    else:
        return {
            "success": False,
            "plate_number": plate_number,
            "message": f"未找到车牌号 {plate_number} 的停车记录。请确认车牌号是否正确。"
        }


def get_shop_info(shop_name):
    """
    获取店铺信息

    Args:
        shop_name: 店铺名称

    Returns:
        dict: 包含店铺详细信息或错误信息
    """
    print(f"DEBUG: Tool [get_shop_info] called with shop_name='{shop_name}'")

    # 支持模糊匹配（不区分大小写）
    for key, shop in SHOPS.items():
        if shop_name.lower() in key.lower():
            return {
                "success": True,
                "shop": shop,
                "message": f"{shop['name']} 位于 {shop['location']}。{shop['description']}"
            }

    return {
        "success": False,
        "shop_name": shop_name,
        "message": f"未找到名为 '{shop_name}' 的店铺。您可以询问客服中心或查看商场导览图。"
    }


def add_points(user_id, amount, reason):
    """
    增加用户积分（用于打卡任务、游戏奖励等）

    Args:
        user_id: 用户 ID
        amount: 增加的积分数量
        reason: 积分来源原因

    Returns:
        dict: 包含当前总积分和操作信息
    """
    print(f"DEBUG: Tool [add_points] called with user_id='{user_id}', amount={amount}, reason='{reason}'")

    total_points = USER_STATE.add_points(user_id, amount)

    return {
        "success": True,
        "user_id": user_id,
        "points_added": amount,
        "total_points": total_points,
        "reason": reason,
        "message": f"恭喜！您因 '{reason}' 获得 {amount} 积分。当前总积分: {total_points}"
    }


def redeem_coupon(user_id, coupon_type, points_cost):
    """
    兑换优惠券（扣除积分并生成优惠券代码）

    Args:
        user_id: 用户 ID
        coupon_type: 优惠券类型（如 "咖啡券", "购物折扣券"）
        points_cost: 需要扣除的积分

    Returns:
        dict: 包含优惠券代码或错误信息
    """
    print(f"DEBUG: Tool [redeem_coupon] called with user_id='{user_id}', coupon_type='{coupon_type}', points_cost={points_cost}")

    current_points = USER_STATE.get_points(user_id)

    if current_points < points_cost:
        return {
            "success": False,
            "user_id": user_id,
            "current_points": current_points,
            "points_needed": points_cost,
            "message": f"积分不足。您当前有 {current_points} 积分，需要 {points_cost} 积分才能兑换 {coupon_type}。"
        }

    # 扣除积分
    USER_STATE.deduct_points(user_id, points_cost)

    # 生成优惠券代码
    import random
    import string
    coupon_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # 添加到用户优惠券列表
    coupon = {
        "type": coupon_type,
        "code": coupon_code,
        "points_cost": points_cost
    }
    USER_STATE.add_coupon(user_id, coupon)

    remaining_points = USER_STATE.get_points(user_id)

    return {
        "success": True,
        "user_id": user_id,
        "coupon_type": coupon_type,
        "coupon_code": coupon_code,
        "points_deducted": points_cost,
        "remaining_points": remaining_points,
        "message": f"兑换成功！您的 {coupon_type} 代码是: {coupon_code}。剩余积分: {remaining_points}"
    }


# ==================== Claude 工具定义 (Anthropic API Format) ====================

TOOL_DEFINITIONS = [
    {
        "name": "find_parking",
        "description": "查找用户车辆的停车位置。当用户询问 '我的车停在哪里' 或提供车牌号时调用此工具。支持迪拜常见车牌格式（如 DXB-1234）。",
        "input_schema": {
            "type": "object",
            "properties": {
                "plate_number": {
                    "type": "string",
                    "description": "车牌号，例如 'DXB-1234'、'AD-9999' 等"
                }
            },
            "required": ["plate_number"]
        }
    },
    {
        "name": "get_shop_info",
        "description": "获取商场内店铺的位置、楼层和详细信息。当用户询问某个品牌或店铺的位置时调用。支持模糊匹配店铺名称。",
        "input_schema": {
            "type": "object",
            "properties": {
                "shop_name": {
                    "type": "string",
                    "description": "店铺名称，例如 'Hermès'、'Apple Store'、'% Arabica' 等"
                }
            },
            "required": ["shop_name"]
        }
    },
    {
        "name": "add_points",
        "description": "为用户增加积分。当用户完成打卡任务、赢得互动游戏、参与商场活动时调用此工具。积分可用于后续兑换优惠券。",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "用户唯一标识符"
                },
                "amount": {
                    "type": "integer",
                    "description": "增加的积分数量，必须为正整数"
                },
                "reason": {
                    "type": "string",
                    "description": "积分来源原因，例如 '完成打卡任务'、'赢得猜谜游戏'、'参与抽奖活动' 等"
                }
            },
            "required": ["user_id", "amount", "reason"]
        }
    },
    {
        "name": "redeem_coupon",
        "description": "使用积分兑换优惠券。当用户请求兑换优惠券或使用积分时调用。会自动检查用户积分是否足够，扣除积分后返回唯一的优惠券代码。",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "用户唯一标识符"
                },
                "coupon_type": {
                    "type": "string",
                    "description": "优惠券类型，例如 '咖啡券'、'10% 购物折扣券'、'免费停车券' 等"
                },
                "points_cost": {
                    "type": "integer",
                    "description": "兑换所需的积分数量"
                }
            },
            "required": ["user_id", "coupon_type", "points_cost"]
        }
    }
]


# ==================== 辅助函数 ====================

def print_all_shops():
    """打印所有店铺信息（用于测试）"""
    print("\n=== 商场店铺列表 ===")
    for shop in SHOPS.values():
        print(f"- {shop['name']} ({shop['category']}) - {shop['floor']}")


def print_user_status(user_id):
    """打印用户状态（用于测试）"""
    user = USER_STATE.get_user(user_id)
    print(f"\n=== 用户 {user_id} 状态 ===")
    print(f"积分: {user['points']}")
    print(f"优惠券: {len(user['coupons'])} 张")
    for coupon in user['coupons']:
        print(f"  - {coupon['type']}: {coupon['code']}")


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("迪拜商场互动服务 Agent - Mock Data 测试\n")

    # 测试店铺查询
    print("1. 测试店铺查询:")
    result = get_shop_info("Hermès")
    print(f"   结果: {result['message']}\n")

    # 测试停车查询
    print("2. 测试停车查询:")
    result = find_parking("DXB-1234")
    print(f"   结果: {result['message']}\n")

    # 测试积分系统
    print("3. 测试积分系统:")
    result = add_points("user_001", 50, "完成打卡任务")
    print(f"   结果: {result['message']}\n")

    # 测试优惠券兑换
    print("4. 测试优惠券兑换:")
    result = redeem_coupon("user_001", "咖啡券", 30)
    print(f"   结果: {result['message']}\n")

    # 打印用户状态
    print_user_status("user_001")

    print("\n所有测试完成！")
