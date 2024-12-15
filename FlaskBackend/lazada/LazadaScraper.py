import requests
import time
from pymongo import MongoClient
from bson.json_util import dumps

def main():
    # Kết nối tới MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['lazada']  
    products_collection = db['dien-thoai-di-dong_3']  

    def get_infos_item(tab_name, tab_id, page):
        url = f"https://www.lazada.vn/{tab_name}/?ajax=true&isFirstRequest=true&page={page}&spm=a2o4n.searchlistcategory.cate_1.1.3539202d4FODU4"
        headers = {
            # Thêm headers nếu cần
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'bx-v': '2.5.22',
            'cookie': '__wpkreporterwid_=a0508f4c-2cbe-426d-a0d3-9baf43cb78e5; miidlaz=miidgislnf1i7asoe1qdulm; lzd_cid=13909879-3eae-4b16-b5ea-98f0c9239784; hng=VN|vi|VND|704; hng.sig=zdydsNS1SsmgPDnK6hvJok_XUpANfcD7ya93aWHPt94; lwrid=AgGS1fl86HE2Nm9X7vybX39uI5ay; lzd_click_id=clkgg5ufp1ibp2p4ubfgup; lzd_sid=1526a2daf191c07d37998adb771c977e; _tb_token_=9bfb6e6db3b7; _m_h5_tk=2d0ce1f858a494d91c2a2733d375e099_1730965841039; _m_h5_tk_enc=0a637f328580d42cbc421ec22432d797; x5sectag=132158; t_fv=1730955404950; t_uid=yBHeQq7EaVZtBIytlYIhhIAaCJXYhPsA; t_sid=B7UeFynAssCk3SAJCb58EfQXcpoj8ehE; utm_channel=NA; lwrtk=AAEEZyy5DNqHds42PCAfy9brF8IFanrfWa3r1ECTh77CtaJOWSCp230=; x5sec=7b22617365727665722d6c617a6164613b33223a22617c43496d5273626b47454d664e677676392f2f2f2f2f77456943584a6c5932467764474e6f5954446b703675382f762f2f2f2f3842536c49774e4441345a6d59774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4445774d4441774d4441774d4441774d4451334e6a51334f4463794e5455354f444e6a4d6d557a4d44426d4f444d354f444d774d4441774d4441774d444178222c22733b32223a2236383438643933663866663830306338227d; EGG_SESS=S_Gs1wHo9OvRHCMp98md7Lr9g2ptE7TslUXSyhLhVZFyHA8FKDPDxEqtRJqH9OD5VDKisNJPIVcRk61vHJOZXVrI0MK-HIQYKtQqIOjVO_0R9hq1A85lwRv6gNgjtQJqfLWIa6y4izMm0_J8Q3Ql0YWTdiJxt0DNnYcTPGmuvCE=; tfstk=f3XjTbwgqq0j9JP4OcEyPyrvAN9_YNwefctOxGHqXKpxWVIpzdrm_Sx6CUse_EB1jAtOXNqD7oVPmivMByzUYJScmLGPqDBX64HRqHtxHaL9_RJMByzzUrx2tdbHBNV56gEWbhutMNdA2QKByhhvBNLJwHKEkdQ9BuTJxhl9Dxdv2LKMyFp9BNp-wjv7z3F6kiZrp30fiPJhDUMC-TtACjjXPWVFF_92JATSBABWDgcp0dkQ_eCHuB8dy8kXCgK1uU7LpY9JO6jwfZwjHK5RZtvVUygwGNTv_TOSkjKBhEOdHQeUqKOONT9VHPch4gTvOL5zZrRwhZ1H-IFurNsWuNBXwqay76SPHQ_LzY_M16jwfZwjHwIylv8CX0hsTxM6Ver7VfcGCunodJpuT6Rvq3DQVugjoIKkVeq7Vf0XM3xoduZSlqf..; epssw=7*GeFss6pWfE8ECeDj7BDs6uoL2ZXOndwZs67gH-obLrsJ_8XTmw-gI0IOrDKNsuojT2ajNgIMUs3vTeDjss3vvBo-hkhWnJh6FGr_LwLTSasvY7Jkss3qGwbgHJgX0j7srSUbhsvM6jUPaTu_VUFdNVjOxMGxWDMyMzDdlrMfvluSIb5vuAeJEIg1usuJn65sOtui-RQf-bbK9EGROO9SAdlOussxHXOOOiOO-d9OOB76z66h_s3Vzsp0Nz4E_u6WC-pCgua8N6zx3xjhlmjOss0HEkBl4zicOReJgxwXssImlVM_; isg=BDs7ynTK2G5xa-Uotg9QJ1Adyh-lkE-SECfRpS34EDpRjFtutWO641bKojTCrKeK',
            'priority': 'u=1, i',
            'referer': 'https://www.lazada.vn/',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-csrf-token': '9bfb6e6db3b7'
        }

        response = requests.get(url, headers=headers)
        data_json = response.json()

        if 'mods' in data_json and 'listItems' in data_json['mods']:
            list_items = data_json['mods']['listItems']
            result = []
            for item in list_items:
                name = item.get('name', 'N/A')
                price = item.get('priceShow', 'N/A')
                image_url = item.get('image', 'N/A')
                item_id = item.get('itemId', 'N/A')
                item_sold_cnt_show = item.get('itemSoldCntShow', 'N/A')
                location = item.get('location', 'N/A')

                # Tạo cấu trúc dữ liệu cho sản phẩm
                item_data = {
                    'name': name,
                    'priceShow': price,
                    'imageUrl': image_url,
                    'itemId': item_id,
                    'itemSoldCntShow': item_sold_cnt_show,
                    'location': location,
                    'reviews': []  # Khởi tạo danh sách đánh giá rỗng
                }
                result.append(item_data)
            return result
        else:
            return "Không tìm thấy trường 'listItems' trong 'mods'."

    def get_review(itemId):
        page = 1
        reviews = []  # Danh sách lưu trữ đánh giá
        while True:
            url = f"https://my.lazada.vn/pdp/review/getReviewList?itemId={itemId}&pageSize=5&filter=0&sort=0&pageNo={page}"
            headers = {
        'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'miidlaz=miidgislnf1i7asoe1qdulm; lzd_cid=13909879-3eae-4b16-b5ea-98f0c9239784; hng=VN|vi|VND|704; hng.sig=zdydsNS1SsmgPDnK6hvJok_XUpANfcD7ya93aWHPt94; lwrid=AgGS1fl86HE2Nm9X7vybX39uI5ay; lzd_click_id=clkgg5ufp1ibp2p4ubfgup; lzd_sid=1526a2daf191c07d37998adb771c977e; _tb_token_=9bfb6e6db3b7; _m_h5_tk=2d0ce1f858a494d91c2a2733d375e099_1730965841039; _m_h5_tk_enc=0a637f328580d42cbc421ec22432d797; t_fv=1730955404950; t_uid=yBHeQq7EaVZtBIytlYIhhIAaCJXYhPsA; t_sid=B7UeFynAssCk3SAJCb58EfQXcpoj8ehE; utm_channel=NA; lwrtk=AAEEZyy5DNqHds42PCAfy9brF8IFanrfWa3r1ECTh77CtaJOWSCp230=; x5sec=7b22617365727665722d6c617a6164613b33223a22617c43496d5273626b47454d664e677676392f2f2f2f2f77456943584a6c5932467764474e6f5954446b703675382f762f2f2f2f3842536c49774e4441345a6d59774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4445774d4441774d4441774d4441774d4451334e6a51334f4463794e5455354f444e6a4d6d557a4d44426d4f444d354f444d774d4441774d4441774d444178222c22733b32223a2236383438643933663866663830306338227d; tfstk=f3XjTbwgqq0j9JP4OcEyPyrvAN9_YNwefctOxGHqXKpxWVIpzdrm_Sx6CUse_EB1jAtOXNqD7oVPmivMByzUYJScmLGPqDBX64HRqHtxHaL9_RJMByzzUrx2tdbHBNV56gEWbhutMNdA2QKByhhvBNLJwHKEkdQ9BuTJxhl9Dxdv2LKMyFp9BNp-wjv7z3F6kiZrp30fiPJhDUMC-TtACjjXPWVFF_92JATSBABWDgcp0dkQ_eCHuB8dy8kXCgK1uU7LpY9JO6jwfZwjHK5RZtvVUygwGNTv_TOSkjKBhEOdHQeUqKOONT9VHPch4gTvOL5zZrRwhZ1H-IFurNsWuNBXwqay76SPHQ_LzY_M16jwfZwjHwIylv8CX0hsTxM6Ver7VfcGCunodJpuT6Rvq3DQVugjoIKkVeq7Vf0XM3xoduZSlqf..; epssw=7*o0Ess6zr069h-BDjssss6s36s0n_jShMvwe3CWobxgf05cXTut0r2XQ8rDKdFlss63seAlDjEEzsu3ohN63vTassssssFE3zsMmc3y5uwNOO22LTPssdAmJkssInvhI1JfnjeSh0JYwxuzLJJiX3qEMTVUT8b9jOxMGBudMyn-m872iqb3oRd_YlOb_JEVQrCdpKDjEuOiQQnXjKY1cEsEEd-HP9BVy7C7AO730V2ppddYBdZiOtOvYnuEhUwSah33hhc6mR90Ci_3iMQxPHo9Yh3xjhsaRbO732-a33_g02Zsce7-S5ssusVkjVjFK9TXjh1dObOAJuopy.; isg=BGdnW6QJzFLMb0ksgiMkaxz59psx7DvOzEN9oTnUG_ZPKIXqQb_SH_xqTjC2wBNG; client_type=desktop',
            'origin': 'https://www.lazada.vn',
            'priority': 'u=1, i',
            'referer': 'https://www.lazada.vn/',
            'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'x-csrf-token': '9bfb6e6db3b7',
            'x-requested-with': 'XMLHttpRequest',
            'x-ua': '140#XgQn56wKzzP12zo24Fsz+pScLBDHdAF6Ny6McyNkBdyP4x5vATd4m4jKPpmtKdtjMv9RP4KiLb9zlp1zzX2SLUY09QzxVnUy9phqzFzb22U+l61cEPn7VMgB/5nqlKJUFbTKzFFI2XMvl61zzPovzSNfGQxLMZ2aMXKkma/cY4LZZOoRsqPznpk8oZOhrWmtUKZfBAf+99t6/joh7KYGqQJyCAuGG48atYHdZexj8LGmN8g+89WNCvlmgKQxfm5ARTXHGBBcMT9Ye4wjeR7gdIsi8GhavHBqDmyq3FuSU/8lzU/Kz8serEEfgQNo7lzArTOr8xai2v++67lcT0p8wDeZ+Fob6N4g8i5hXS4soNDg5B/b5iyaQgy1deMSs3ySWYPC/Sj2b5ZAR8rvqj4tVMckj8ZLQbMueI9ywK08xB/JsUBjPXvYjAUgpdits8BjDJRST45F5PJ5qA8WPgui/JQfd6eWGFLpgbdyVOKV2sq85ZGcsBuzW6q29GtmZ8bjX+lVdkoGRv9pHhTdud0md5Nfj5gWghcsBJXjwyaJ/8lc0Bf42ZylGgUWRMdGy25K/zeGrJ0pdUxJGXkCkt/ZbKUZMpxpTe5vY84+yG2wB2unBGCgw0rkAKOoh3C3Jui+Pfv8iup2QEnbrlDuMVTpFH5/Y5rJ7oVWZwKd1hM87621LuwMdcSMgPPnIzVYdJ70SzifP1363L9+P5TWMtFaqccjObPQSmT+4gKc4TxzMYiLSbq7AOM6dwRgTS1qWDjbJskzkGsAKIkQp9Z1pALc13sonVz+NqvEIMoX+g2bTamfiPSUv8ga8oAonaSnm/BjrDjlQ1V+2W3qHAtIRnOFLmPjcaCdtAemMFiw8UEXRLfBd6M/vqXpuDEs9hk+erle6WkQtgMj2dMJM+4EyJ8JGw/ksH4qqlo72i3mJ2ry7o0zcLolJIY6kZqiBvcwCkdQSSAUOORSut/MZ8O4mOFdXiGinOfsDc3jYQaMVaSVogiDUnohO4gDbIE2qyB4DEjr1dgY7yfPoaRFrJYlNU8PkDgU1WyBo4ukFIA56DQ6fo3+SWp8cs6wjsfmzDL7vgGIDPE45BEuXeKNso+uJ864hNeuzQRvUKj9L1tACA3m6amFl7iP0aRCLh8+O/rpWRQuu+TlhzQp5hTupT5Ci8YOc/jEdKgs9g0egGyYfprqFQQVJV5bvCda9k62DVP6g2hDHbAiagt2uaMZnQFnmDvr4uUObgshzcTqy9pdpgjjqClIAT9Oeq41QIU8NjPLoD9YbGKCWnc17qBwmAEKphtw4S1ZZtEPYqFdkGuKWmb60d+fgxEp69heYYcxEDTOd/o1y93Mjn6nx9KquGhfQpLh3FZDBtzFUbOy996KrNTAG9kpMoqsrg2ZyGGa6BZUENQq3v3s/csWZ8XYk8OZLgB/dukCK6M0BwTu4ZsivAzAVu5hZAi7Nyz/0Cr28hoQoM6eSDBLrcCFt1sebr6a53un955AuE1qI4ieRkquFR6j+39M3lDDGMZsenB0v6M2uLtm2Omd3fM2vhsDKhQimhYxgkTE3eqk4VLvtxdB5OUxle5B1aJwUEhnR7QJ74OMrXsHSKtYtjsib9WRaN+xreu68uvQ3NBUgxf67Lbw1uMotjvVfLuBF/8UWl1KU2v4bOUMwXV53r7wkwfcG4LFeWVENWfM4hbrUl86/1uDIv9nteEy/sXxmw8cWQWh88zgB0CHklAGCT1rJx/+0cofA+7NjvpVhp/2HNy+oH0JDnVyOVQNek42ROdGJA2Hl0gFzRF3ZPrIGibeFEehl6dVRryqv/g6PtHlDXXGr2W/95Zi8vyUDSYuEg7/kgP56VhgLuwTHS9ECRHhMV1Gk1O/VoNu5+9O/N/R5EvyV0WSfYk1siyWWOZcyElgUT/JLGncrzJNw7a7kzDGWNg/gE/gipRSrqTcQYH+ONlVE5aCQR0kGwO3xgknf9/2WFhwVYa6D7jHCE+23gDpsIIxlFaAnnWNf8m0cjuizLoDjQJq27dUC8znhcUpf6R7/0ibUecDQS3Q5odTB00hLkFTybH2yPd8hKLEdJ7X6XUqVrIAMtcAcyJ0XWvG+l0SfmePdD+FsglGu5fmcRjWOOcumZh0TAS7p8TNOcCumkK207P+ufvqBppL0hpttVZ/Y5u1JT9hUU2ZiHRDUqjNLSX7iP4U3Oal4I34Pn5eGgb0uRkbBFyX0PQjIysgFvZRxcYYpNyyvduGul+=',
            'x-umidtoken': 'T2gACIn-djG-N7hrUhiRy8eKwcirxMtHZvil-cXlnK3eY4wa4pf7J0E0ux0qJwxZMVU='
            }

            response = requests.get(url, headers=headers)
            data_json = response.json()

            if response.status_code == 200:
                data = response.json()
                if 'model' in data and 'items' in data['model']:
                    review_items = data['model']['items']
                    if not review_items:  # Nếu không còn đánh giá, thoát vòng lặp
                        print("Không còn đánh giá nào.")
                        break
                    
                    for review in review_items:
                        rating = review.get('rating')
                        review_content = review.get('reviewContent')
                        review_time = review.get('reviewTime')
                        sku_id = review.get('skuId')
                        sku_info = review.get('skuInfo')
        
                        # Tạo cấu trúc dữ liệu cho đánh giá
                        review_data = {
                            'rating': rating,
                            'reviewContent': review_content,
                            'reviewTime': review_time,
                            'skuId': sku_id,
                            'skuInfo': sku_info
                        }
                        time.sleep(2)

                        reviews.append(review_data)  # Thêm đánh giá vào danh sách

                    page += 1  # Chuyển sang trang tiếp theo
                else:
                    print("Không tìm thấy đánh giá.")
                    break
            else:
                print(f"Không thể lấy dữ liệu. Mã trạng thái: {response.status_code}")
                break
        
        return reviews  # Trả về danh sách đánh giá

    # Định nghĩa các tab bạn muốn lấy dữ liệu
    tabs = [
        # Electronic Devices
        {'name': 'dien-thoai-di-dong', 'id': 4518},
        {'name': 'may-tinh-bang', 'id': 4519},
        {'name': 'laptop', 'id': 4414},
        {'name': 'may-tinh-de-ban-va-phu-kien', 'id': 4417},
        {'name': 'am-thanh', 'id': 10100387},
        {'name': 'camera-giam-sat-2', 'id': 15262},
        {'name': 'may-anh-may-quay-phim', 'id': 4404},
        {'name': 'may-quay-phim', 'id': 4499},
        {'name': 'man-hinh-vi-tinh', 'id': 4474},
        {'name': 'man-hinh-may-in', 'id': 10100380},
        {'name': 'dong-ho-thong-minh', 'id': 10100415},
        {'name': 'dieu-khien-choi-game', 'id': 10100424},
        # Electronic Accessories
        {'name': 'phu-kien-dien-thoai-may-tinh-bang', 'id': 4522},
        {'name': 'thiet-bi-thong-minh', 'id': 10100412},
        {'name': 'thiet-bi-so', 'id': 6146},
        {'name': 'phu-kien-may-anh-may-quay-phim', 'id': 4502},
        {'name': 'phu-kien-may-bay-camera', 'id': 11092},
        {'name': 'thiet-bi-luu-tru-2', 'id': 10100386},
        {'name': 'phu-kien-may-vi-tinh', 'id': 4455},
        {'name': 'linh-kien-may-tinh', 'id': 4419},
        {'name': 'phu-kien-ong-kinh', 'id': 9732},
        {'name': 'thiet-bi-mang', 'id': 4486},
        {'name': 'phu-kien-may-choi-game', 'id': 10100439},
        # TV & Home Appliances
        {'name': 'tv-video-am-thanh-thiet-bi-deo-cong-nghe', 'id': 4403},
        {'name': 'do-gia-dung-nho', 'id': 4400},
        {'name': 'do-gia-dung-lon', 'id': 10100871},
        {'name': 'phu-kien-cho-tv', 'id': 11514},
        # Health & Beauty
        {'name': 'cham-soc-da-mat', 'id': 2277},
        {'name': 'trang-diem', 'id': 4611},
        {'name': 'dung-cu-cham-soc-sac-dep', 'id': 4948},
        {'name': 'san-pham-tam-cham-soc-co-the', 'id': 4762},
        {'name': 'san-pham-cham-soc-toc', 'id': 4879},
        {'name': 'cham-soc-ca-nhan', 'id': 4956},
        {'name': 'cham-soc-cho-nam-gioi', 'id': 4863},
        {'name': 'nuoc-hoa', 'id': 4839},
        {'name': 'thuc-pham-bo-sung', 'id': 4741},
        {'name': 'thuc-pham-cho-sac-dep', 'id': 6782},
        {'name': 'ho-tro-tinh-duc', 'id': 12398},
        {'name': 'thiet-bi-y-te', 'id': 7174},
        # Babies & Toys
        {'name': 'ta-dung-cu-ve-sinh', 'id': 10601},
        {'name': 'sua-cong-thuc-bot-an-dam', 'id': 10100747},
        {'name': 'quan-ao-phu-kien-cho-be', 'id': 10809},
        {'name': 'do-dung-bu-sua-an-dam', 'id': 10551},
        {'name': 'xe-ghe-em-be', 'id': 10731},
        {'name': 'cham-soc-tre-so-sinh-tre-nho', 'id': 10632},
        {'name': 'tam-cham-soc-co-the-tre-so-sinh', 'id': 14986},
        {'name': 'do-choi-tro-choi', 'id': 10216},
        {'name': 'xe-mo-hinh-tro-choi-dieu-khien-tu-xa', 'id': 10223},
        {'name': 'the-thao-tro-choi-ngoai-troi', 'id': 10222},
        {'name': 'do-choi-cho-tre-so-sinh-chap-chung', 'id': 10327},
        {'name': 'do-choi-giao-duc-tre-em', 'id': 10386},
        # Groceries & Pets
        {'name': 'bach-hoa-online-sua-uht-tiet-trung-sua-bot', 'id': 14467},
        {'name': 'cac-loai-do-uong', 'id': 8895},
        {'name': 'shop-Thuc-pham-tu-sua-do-lanh', 'id': 10003009},
        {'name': 'shop-do-hop', 'id': 10003059},
        {'name': 'shop-So-co-la-Snack-Keo', 'id': 10003010},
        {'name': 'shop-Nguyen-lieu-nau-an-lam-banh', 'id': 10003011},
        {'name': 'bach-hoa-online-chat-lau-chui-nha-cua', 'id': 14442},
        {'name': 'bach-hoa-online-muong-nia-nhua', 'id': 14698},
        {'name': 'bach-hoa-online-giat-ui', 'id': 10100539},
        {'name': 'phu-kien-cho-thu-cung', 'id': 10100631},
        {'name': 'thuc-an-thu-cung', 'id': 10100629},
        {'name': 'shop-rau-cu-qua', 'id': 14365},
        # Home & Lifestyle
        {'name': 'do-dung-bep-phong-an', 'id': 12648},
        {'name': 'tan-trang-nha-cua', 'id': 12646},
        {'name': 'dung-cu-dien', 'id': 12667},
        {'name': 'dung-cu-cam-tay-da-nang', 'id': 12666},
        {'name': 'do-dung-phong-ngu-gia-dinh', 'id': 12651},
        {'name': 'do-dung-phu-kien-phong-tam', 'id': 12650},
        {'name': 'cac-loai-den', 'id': 12681},
        {'name': 'san-pham-trang-tri-nha-cua', 'id': 12654},
        {'name': 'san-pham-noi-that', 'id': 12652},
        {'name': 'van-phong-pham-va-nghe-thu-cong', 'id': 12649},
        {'name': 'truyen-thong-am-nhac-sach', 'id': 3194},
        {'name': 'dung-cu-ve-sinh-2', 'id': 12647},
        # Women's Fashion & Accessories
        {'name': 'trang-phuc-nu', 'id': 6394},
        {'name': 'giay-nu-thoi-trang', 'id': 6245},
        {'name': 'do-ngu-noi-y', 'id': 6403},
        {'name': 'phu-kien-cho-nu', 'id': 7811},
        {'name': 'tui-cho-nu', 'id': 14236},
        {'name': 'trang-suc-nu', 'id': 8027},
        {'name': 'dong-ho-nu-thoi-trang', 'id': 8944},
        {'name': 'kinh-deo-mat-nu', 'id': 13329},
        {'name': 'kinh-mat-danh-cho-nu', 'id': 13326},
        # Men's Fashion & Accessories
        {'name': 'trang-phuc-nam', 'id': 6413},
        {'name': 'giay-nam-thoi-trang', 'id': 6315},
        {'name': 'do-lot-nam', 'id': 6420},
        {'name': 'phu-kien-thoi-trang-nam', 'id': 7890},
        {'name': 'tui-nam', 'id': 14237},
        {'name': 'trang-suc-nam', 'id': 4014},
        {'name': 'dong-ho-nam-gioi', 'id': 8839},
        {'name': 'kinh-deo-mat-nam', 'id': 13331},
        {'name': 'kinh-mat-danh-cho-nam', 'id': 13328},
        {'name': 'trang-phuc-cua-be-trai', 'id': 1727},
        {'name': 'thoi-trang-giay-cho-be-trai', 'id': 1785},
        {'name': 'trang-phuc-cua-be-gai', 'id': 1800},
        {'name': 'thoi-trang-giay-danh-cho-be-gai', 'id': 1777},
        {'name': 'tui-danh-cho-tre-em', 'id': 14239},
        {'name': 'dong-ho-danh-cho-tre-em', 'id': 8970},
        {'name': 'kinh-mat-danh-cho-tre-em', 'id': 13328},
        {'name': 'quan-ao-the-thao-be-gai', 'id': 7560},
        {'name': 'quan-ao-the-thao-be-trai', 'id': 7563},
        {'name': 'do-the-thao-cho-be-gai', 'id': 7477},
        {'name': 'do-the-thao-cho-be-trai', 'id': 7479},
        
        # Sports & Travel
        {'name': 'do-the-thao-nam', 'id': 7475},
        {'name': 'quan-ao-the-thao-cho-nam', 'id': 7527},
        {'name': 'do-the-thao-nu', 'id': 7473},
        {'name': 'quan-ao-the-thao-cho-nu', 'id': 7483},
        {'name': 'vali-ba-lo-tui-du-lich-2', 'id': 14240},
        {'name': 'hoat-dong-da-ngoai', 'id': 6593},
        {'name': 'dung-cu-de-tap-the-hinh', 'id': 6590},
        {'name': 'cac-mon-the-thao-vot', 'id': 6591},
        {'name': 'cac-mon-tap-luyen-doi-khang', 'id': 6592},
        {'name': 'dam-boc-vo-thuat-danh-mma', 'id': 12104},
        {'name': 'cac-mon-the-thao-duoi-nuoc', 'id': 12049},
        {'name': 'phu-kien-the-thao', 'id': 11510},
        
        # Automotive & Motorcycles
        {'name': 'xe-mo-to-xe-tay-ga', 'id': 10100714},
        {'name': 'cham-soc-o-to', 'id': 10100702},
        {'name': 'phu-kien-trong-o-to-xe-may', 'id': 8309},
        {'name': 'phu-kien-ngoai-o-to-xe-may', 'id': 8302},
        {'name': 'bo-phan-phu-tung-thay-the-cho-xe', 'id': 13279},
        {'name': 'hang-dien-tu-2', 'id': 10100703},
        {'name': 'dau-nhot-o-to-xe-may', 'id': 8338},
        {'name': 'bo-phan-mo-to-phu-tung-thay-the-cho-mo-to', 'id': 13299},
        {'name': 'do-bao-ho-mo-to', 'id': 13303},
        {'name': 'phu-kien-gan-ngoai-mo-to', 'id': 13302},
        {'name': 'dau-nhot-mo-to', 'id': 13300},
        {'name': 'banh-xe-lop-xe-may', 'id': 12381},
        
        # Digital Goods
        {'name': 'mobilerecharge?wh_weex=true', 'id': 15270},
        {'name': 'voucher-am-thuc', 'id': 15040},
        {'name': 'du-lich', 'id': 15043},
        {'name': 'hoat-dong-va-giai-tri', 'id': 15042},
        {'name': 'suc-khoe-va-lam-dep', 'id': 15041},
        {'name': 'the-qua-tang', 'id': 10100018},
        {'name': 'voucher-dich-vu', 'id': 14990}
    ]

    # Vòng lặp qua từng tab và lấy dữ liệu
    for tab in tabs:
        page = 1
        while True:
            print(f"Đang lấy dữ liệu từ tab {tab['name']} trang {page}...")
            items_info = get_infos_item(tab['name'], tab['id'], page)
            
            # Kiểm tra xem kết quả có rỗng hay không
            if isinstance(items_info, str) or not items_info:
                print(f"Không còn nội dung trên trang {page}. Chuyển sang danh mục tiếp theo.")
                break

            # Xử lý và in thông tin sản phẩm
            for item in items_info:
                print(f"itemId: {item['itemId']}, Tên sản phẩm: {item['name']}, Giá: {item['priceShow']}, URL ảnh: {item['imageUrl']}, itemSoldCntShow: {item['itemSoldCntShow']}, location: {item['location']}")
                
                # Lấy đánh giá cho từng sản phẩm
                reviews = get_review(item['itemId'])  # Gọi hàm để lấy đánh giá
                
                # Lưu thông tin sản phẩm và đánh giá vào MongoDB
                item['reviews'] = reviews  # Gán danh sách đánh giá cho sản phẩm
                products_collection.update_one({'itemId': item['itemId']}, {'$set': item}, upsert=True)  # Cập nhật hoặc thêm mới

            page += 1
            time.sleep(40)
        print(f"Đang nghỉ giữa các danh mục, chờ 5 giây trước khi tiếp tục danh mục tiếp theo...")
        time.sleep(5)
    cursor = products_collection.find({})
    with open('lazada/merged_file.json', 'w') as file:
        file.write('[')
        for document in cursor:
            file.write(dumps(document))
            file.write(',')
        file.write(']')

if __name__ == '__main__':
    main()