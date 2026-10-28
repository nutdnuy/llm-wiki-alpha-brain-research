# Editable research flows

[กลับไป README](../../README.md)

ภาพทั้ง 3 ชุดสร้างขึ้นสำหรับ Alpha Research Wiki ไฟล์ `.excalidraw` เป็น
ต้นฉบับที่แก้ไขได้ ส่วน README ใช้ PNG เพื่อแสดงฟอนต์และโลโก้เหมือนกันในทุกเครื่อง
แต่ละภาพมี SVG สำหรับเปิดขยายด้วย

| ภาพ | ต้นฉบับ | ภาพสำหรับอ่าน |
| --- | --- | --- |
| จากหลักฐานสู่บทเรียน | [Excalidraw](flow-overview.excalidraw) | [PNG](../assets/flow-overview.png) · [SVG](../assets/flow-overview.svg) |
| คลังร่วมสำหรับสอง backend | [Excalidraw](flow-two-backends.excalidraw) | [PNG](../assets/flow-two-backends.png) · [SVG](../assets/flow-two-backends.svg) |
| เรียนรู้จากผลทดลอง | [Excalidraw](flow-learning-loop.excalidraw) | [PNG](../assets/flow-learning-loop.png) · [SVG](../assets/flow-learning-loop.svg) |

## แก้ไขภาพ

ดาวน์โหลดไฟล์ `.excalidraw` แล้วเปิดด้วยเมนู Open ของ Excalidraw
กล่อง ข้อความ ลูกศร และภาพโลโก้เป็นองค์ประกอบแยกกัน แก้ไขต่อได้
โลโก้ถูกฝังจากไฟล์ SVG ที่อนุมัติไว้โดยตรง เก็บสัดส่วนเดิมเมื่อย้ายหรือปรับขนาด

ภาพใช้ Quantsera / Material 2 dark: พื้นหลัง `#121212`, พื้นกล่อง `#1E1E1E`,
Purple `#BB86FC` และ Teal `#03DAC6` มีทั้งข้อความและทิศทางลูกศรเพื่อให้อ่านได้
โดยไม่ต้องอาศัยสีเพียงอย่างเดียว เส้นประระบุขั้นตอนรันด้วย workflow ภายนอก

## สร้าง Preview ใหม่

รันจากราก Repo:

```bash
python3 docs/diagrams/render_svg.py
```

สคริปต์นี้อ่าน Scene แล้วสร้าง `docs/assets/flow-*.svg` โดยใช้เฉพาะ Python
standard library และฝัง Roboto จากไฟล์ฟอนต์ใน Repo
รองรับองค์ประกอบที่ใช้ในภาพชุดนี้เท่านั้น เป็น Lightweight preview renderer
ของโปรเจกต์ ไม่ใช่ Official Excalidraw exporter

PNG ใน README สร้างจาก SVG เหล่านี้ด้วย Chromium ที่ขนาด 2× ของ Canvas
และรอให้ฟอนต์โหลดเสร็จก่อนบันทึก ภาพ Overview มีขนาด 2400 × 1240,
Two backends 2400 × 2080 และ Learning loop 2400 × 1520 พิกเซล
เมื่อแก้ Scene ให้สร้าง SVG และ PNG ใหม่พร้อมกัน แล้วตรวจข้อความและเส้นเชื่อมอีกครั้ง

ตัวแก้ไข Excalidraw ใช้ Sans-serif ที่แก้ไขได้ (`fontFamily: 2`)
ส่วน SVG/PNG ใช้ Roboto 400/500 จาก Fontsource 5.2.8
จึงอาจมีความต่างของรูปร่างตัวอักษรเมื่อเปิดใน Editor
การส่งมอบชุดนี้ใช้ไฟล์ใน Repo โดยไม่มีลิงก์ Scene ที่อัปโหลดแยกไปยังบริการ Excalidraw

ดู [ที่มาของ Assets และสิทธิ์ใช้งาน](../assets/README.md) และ
[ผลการตรวจภาพ](../visual-verification.md)
