# SMR Safety Thailand
เรื่องนิวเคลียร์ คุยกันให้เข้าใจได้

แหล่งความรู้ภาษาไทยที่ Roppon Picha ดูแลส่วนบุคคล เชื่อมกับความสนใจด้านงานวิจัยของ วป. ไม่ใช่ช่องทางหรือจุดยืนอย่างเป็นทางการของ สทน.

## อ่านอะไรได้บ้าง
- คำถามง่าย ๆ เกี่ยวกับ SMR safety พร้อมเงื่อนไขและแหล่งอ้างอิง
- ACP100, NuScale US460, BWRX-300, i-SMR และ KLT-40S
- IAEA 19 infrastructure issues และ Milestones Approach
- ความเคลื่อนไหวประเทศไทยและ PDP2026 โดยแยกร่างแผนออกจากการอนุมัติจริง

## Build
ต้องมี Python3.11ขึ้นไป และ Node.js สำหรับทดสอบคะแนน
```sh
python -m pip install -r requirements.txt
python scripts/build.py
node scripts/test-measurement.cjs measurement.js
```
ไฟล์เว็บไซต์พร้อมเผยแพร่อยู่ใน dist/; เนื้อหา Markdown ถูกแปลงเป็น HTML พร้อม style และตรวจลิงก์ภายใน
ถ้าทดสอบซ้ำในเครื่อง ใช้ --output กับโฟลเดอร์ใหม่เพื่อเก็บผลก่อนหน้า ไม่ลบหรือเขียนทับ source

## อัปเดตเนื้อหา
แก้ไฟล์ใน docs/, updates/ หรือ technical-baseline/ -> เปิด pull request -> อ่าน Netlify Deploy Preview -> ตรวจสาระ/ลิงก์ -> merge เมื่อพร้อม
main เป็นสาขาเผยแพร่เมื่อเชื่อม Netlify Git deployment แล้ว
ดู [แนวทางเนื้อหา](CONTRIBUTING.md), [style guide](STYLE_GUIDE.md) และ [แม่แบบข่าว](templates/update-template.md)

## การดูแลข้อมูล
เก็บเฉพาะเนื้อหาที่เหมาะกับสาธารณะ แหล่งอ้างอิง และโค้ดเว็บ
ไฟล์ KPI ภายใน journal ส่วนตัว และข้อมูลผู้อ่านจริงไม่อยู่ใน repo นี้
แบบเช็กความเข้าใจเป็นการเรียนรู้ของแต่ละรอบ ไม่ส่งคำตอบไปยัง backend; เก็บใน memory และให้ผู้ใช้เลือกส่งออกเอง ผู้ให้บริการ hosting อาจมี access logs ตามนโยบายของตน
แบบ3ข้อยังไม่ได้ validated; ไม่ถือว่าคะแนนทดลองของผู้สร้างเป็นผล impact ต่อประชาชน

## บรรณาธิการและสิทธิ์
เนื้อหาเป็นบันทึกอ่านและอธิบายของผู้ดูแล ไม่ใช่คำรับรองแบบเตาหรือคำตัดสินของหน่วยงานกำกับ
เอกสาร/ชื่อเครื่องหมายของบุคคลอื่นยังมีสิทธิ์ของเจ้าของ อ้างลิงก์ต้นทางแทนการนำไฟล์ต้นฉบับมาแจก
ยังไม่ได้ให้ใบอนุญาตแบบ open-source แก่ข้อความ/โค้ดทั้ง repo; ติดต่อผู้ดูแลหากต้องการนำไปใช้ต่อ เก็บ attribution ของต้นทางเสมอ

## แหล่งข้อมูล
[evidence/public-sources.json](evidence/public-sources.json) และ [technical-baseline/evidence/sources.json](technical-baseline/evidence/sources.json)
สถานะหลักฐานและวันที่ตรวจต้องอ่านพร้อมแต่ละรายการ ไม่มีคะแนนจัดอันดับความปลอดภัยหรือการรับรองความพร้อมประเทศไทย