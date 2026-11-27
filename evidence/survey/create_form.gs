/**
 * Tạo Google Form khảo sát theo evidence/survey/questions.md.
 *
 * Cách chạy:
 *   1. Mở https://script.google.com → New project (Dự án mới).
 *   2. Xoá code mẫu, dán toàn bộ file này vào, bấm Save.
 *   3. Chọn hàm createSurveyForm → bấm Run → cấp quyền (Review permissions → chọn tài khoản → Allow).
 *   4. Mở Execution log (Nhật ký thực thi): có link điền form và link sửa form.
 * Mỗi lần Run tạo một form MỚI, không sửa form cũ.
 */
function createSurveyForm() {
  var form = FormApp.create('Khảo sát: khiếu nại khi đặt đồ ăn qua app');
  form.setDescription(
    'Nhóm NPCs (L3B, AI20K) tìm hiểu chuyện khiếu nại khi đặt đồ ăn qua app.\n' +
    'Khoảng 2 phút, ẩn danh, chỉ hỏi chuyện ĐÃ xảy ra với bạn. Không cần ghi tên, số điện thoại, mã đơn.'
  );
  form.setCollectEmail(false);
  form.setConfirmationMessage('Cảm ơn bạn đã dành thời gian! 🙏');

  form.addMultipleChoiceItem()
    .setTitle('1. Bạn thường đặt đồ ăn qua app (ShopeeFood, GrabFood...) khoảng bao nhiêu lần/tháng?')
    .setChoiceValues(['Dưới 1 lần / hầu như không đặt', '1 – 5 lần', '6 – 10 lần', 'Trên 10 lần'])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('2. Bạn từng gặp sự cố nào dưới đây khi nhận đơn? (Có thể chọn nhiều)')
    .setChoiceValues(['Giao thiếu món', 'Giao sai món', 'Giao trễ nhiều (trên 30 phút)', 'Chưa từng gặp'])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('3. Lần gần nhất gặp sự cố, bạn mất bao lâu để được xử lý xong?')
    .setChoiceValues(['Giải quyết ngay trong vòng 5 – 10 phút',
                      'Chờ vài tiếng đến hôm sau',
                      'Bỏ qua không khiếu nại vì thấy rườm rà / mất thời gian',
                      'Chưa từng khiếu nại'])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('4. Bạn thấy vướng hoặc khó chịu nhất ở bước nào khi khiếu nại?')
    .setHelpText('Bỏ qua câu này nếu bạn chưa từng khiếu nại.')
    .setChoiceValues(['Bot trả lời chung chung, vòng vo không đúng vấn đề',
                      'Chờ nhân viên phản hồi / duyệt hoàn tiền quá lâu',
                      'Phải tìm lại hóa đơn giấy, chụp nhiều ảnh bằng chứng',
                      'Không rõ mình có đủ điều kiện được hoàn tiền/voucher hay không'])
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('5. Kể ngắn 1–2 câu về lần khiếu nại nhớ nhất của bạn (hoặc điều bạn muốn được xử lý nhanh hơn):')
    .setRequired(false);

  Logger.log('Link điền form (gửi cho mọi người): ' + form.getPublishedUrl());
  Logger.log('Link sửa form: ' + form.getEditUrl());
}
