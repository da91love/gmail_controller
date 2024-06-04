class EmailMsgCreator:
    @staticmethod
    def get_send_mail_msg(author_unique_id, seeding_num):
        subject = None
        body = None

        if seeding_num == 1:
            subject = 'Paid Opportunity with the Best Kbeauty Toner - Eqqualberry'
            body = f'''
                <div>Hi {author_unique_id},</div>
                <br/>
                <div>This is Jennifer, I’m a brand manager here in Eqqualberry.</div>
                <div><b>We’re a Korean skincare brand</b>, and we at Eqqualberry believe in a strong emphasis on balanced skincare, we are committed to creating clean beauty that is all natural and free from harsh chemicals!</div>
                <br/>
                <div>Your TikTok channel recently caught our eye, and we couldn’t help but be captivated by your genuine passion for beauty products.</div>
                <br/>
                <div>Recently, we went viral and were amazed by how much attention @charinecheungg’s collaboration with us has gotten. It’s not just about the number of views but we were able to see that many TikTok viewers were genuinely interested and are in need of our product. As a result, <b>Eqqualberry’s Swimming Pool Toner is currently ranked 14th overall for toner on Amazon US.</b></div>
                <br/>
                <div>We are excited to share with you that we have <b>recently launched our product on Shopee</b> and this will be available across the Southeast Asian market as well, and <b>we’d love to collaborate with you as one of the first few creators to introduce our product to your audience!😉</b></div>
                <br/>
                <div>To provide you with a clearer picture, please see the following key benefits on our toner!</div>
                <br/>
                <div><b>* Key Benefits:</b></div>
                <ul>
                <li>Ideal for sensitive and reactive skin</li>
                <li>Contain Protease to gently exfoliate skin and keep pores clean</li>
                <li>Deep hydration with five berry extracts and hyaluronic acid</li>
                <li>Refines pores and reduces blackheads</li>
                <li>Fungal acne and acne safe</li>
                </ul>
                <div>Please check out <b>"#eqqualberrySwimmingPoolToner"</b> in Amazon for product details.</div>
                <br/>
                <div>We truly looking forward to potentially collaborating with you, and if you are interested we’d love to speak next steps soon!</div>
                <br/>
                <div>Warmest regards, Jennifer</div>
                
                <span>&nbsp;</span>
                <div>Tiktok: @eqqualberry_us</div>
                <div>Instagram: eqqualberry_us</div>
            '''
        elif seeding_num == 2:
            subject = 'Re-Collaboration offer with Eqqualberry'
            body = f'''
                <div>Hi {author_unique_id},</div>
                <div>I'm Jennifer from Eqqualberry.</div>
                <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                <div>So I'd like to suggest a second collaboration.</div>
                <br/>
                <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                <div>Warmest regards, Jennifer</div>

                <span>&nbsp;</span>
                <div>Tiktok: @eqqualberry_us</div>
                <div>Instagram: eqqualberry_us</div>
            '''

        else:
            subject = 'Re-Collaboration offer with Eqqualberry'
            body = f'''
                <div>Hi {author_unique_id},</div>
                <div>I'm Jennifer from Eqqualberry.</div>
                <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                <div>So I'd like to suggest a third collaboration.</div>
                <br/>
                <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                <div>Warmest regards, Jennifer</div>

                <span>&nbsp;</span>
                <div>Tiktok: @eqqualberry_us</div>
                <div>Instagram: eqqualberry_us</div>
            '''

        return {
            'subject': subject,
            'body': body,
        }

    # body = f'''
    #      <div>Hi {author_unique_id},</div>
    #      <div>I'm Jennifer from Eqqualberry.</div>
    #      <br/>
    #      <div>As I mentioned earlier, due to our system I start a new email thread to discuss additional contract details.</div>
    #      <br/>
    #      <div>Let's discuss next step of collaboration through this email thread!</div>
    #      <div>Warmest regards, 🌷Jennifer</div>
    #
    #      <span>&nbsp;</span>
    #      <div>Tiktok: @eqqualberry_us</div>
    #      <div>Instagram: eqqualberry_us</div>
    #  '''