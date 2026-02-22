from flask import render_template, request, redirect, url_for, flash
from app import app, mail, db
from app.models import ContactMessage, VolunteerApplication, PartnerApplication
from app.utils import rate_limit, sanitize_email, sanitize_amount, sanitize_text, sanitize_phone, add_security_headers
from flask_wtf.csrf import CSRFError
from flask_mail import Message
import os
from threading import Thread
from sqlalchemy import func


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("✅ Email sent successfully")
        except Exception as e:
            print(f"❌ Error sending email: {e}")


def get_unique_member_count() -> int:
    """
    Count unique people across volunteers AND partners by email.
    If someone registers as both, they count as 1.
    """
    volunteer_emails = db.session.query(
        func.lower(VolunteerApplication.email)
    ).distinct()
    partner_emails = db.session.query(
        func.lower(PartnerApplication.email)
    ).distinct()
    return len(volunteer_emails.union(partner_emails).all())


    # result = db.session.execute(db.text("""
    #     SELECT COUNT(*) FROM (
    #         SELECT LOWER(email) AS email FROM volunteer_applications
    #         UNION
    #         SELECT LOWER(email) AS email FROM partner_applications
    #     ) AS unique_members
    # """))
    # return result.scalar() or 0

# ============================================================
# PUBLIC ROUTES
# ============================================================

@app.route("/")
def home():
    total_members = get_unique_member_count()
    return render_template("public/home.html", total_members=total_members)


@app.route("/about/who-we-are")
def about():
    return render_template("public/about.html")


@app.route("/about/team")
def teams():
    return render_template("public/teams.html")


@app.route("/thematic/climate-resilience-and-adaptation")
def climate():
    return render_template("public/climate.html")


@app.route("/thematic/water-sanitation-and-hygiene")
def water():
    return render_template("public/water.html")


@app.route("/thematic/environmental-sustainability-circuar-economy-and-waste-management")
def environment():
    return render_template("public/environment.html")


@app.route("/thematic/youth-empowerment-and-capacity-building")
def youth():
    return render_template("public/youth.html")


@app.route("/thematic/climate-education-and-public-awareness")
def education():
    return render_template("public/education.html")


@app.route("/thematic/research-innovation-and-policy-advocacy")
def research():
    return render_template("public/research.html")


@app.route("/projects-and-impacts")
def projects():
    return render_template("public/projects.html")


@app.route("/media")
def media():
    return render_template("public/media.html")


@app.route("/resources/news-and-updates")
def news():
    return render_template("public/news.html")


@app.route("/resources/publications")
def publications():
    return render_template("public/publications.html")


@app.route("/get-in-touch/contact-us")
def contact():
    return render_template("public/contact.html")


@app.route("/get-in-touch/contact-us/sending-mail", methods=["GET", "POST"])
def send_mail():
    if request.method == "POST":
        name = sanitize_text(request.form.get("name", ""))
        email = sanitize_email(request.form.get("email", ""))
        number = sanitize_phone(request.form.get("number", ""))
        message = sanitize_text(request.form.get("message", ""))
        subject = "ClimateWISE Youth Organization"

        if not all([name, email, number, message]):
            flash("All fields are required", category="error")
            return redirect(url_for("contact"))

        if not email:
            flash("Please enter a valid email address.", category="error")
            return redirect(url_for("contact"))

        try:
            msg = Message(
                subject,
                sender=os.getenv("USER_EMAIL"),
                recipients=[os.getenv("USER_EMAIL"), "saviourb100@gmail.com"]
            )
            msg.body = (
                f"Message from: {name}\n"
                f"Email: {email}\n"
                f"Phone Number: {number}\n"
                f"Subject: {subject}\n\n"
                f"Description: {message}"
            )
            Thread(target=send_async_email, args=(app, msg)).start()

            new_message = ContactMessage(
                name=name, email=email, number=number, message=message
            )
            db.session.add(new_message)
            db.session.commit()

            flash("Message sent successfully!", category="success")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("Failed to send message. Please try again later.", category="error")

        return redirect(url_for("contact"))


@app.route("/get-in-touch/volunteers")
def volunteer():
    return render_template("public/volunteer.html")


@app.route("/get-in-touch/volunteers/sending-details", methods=["POST"])
def send_details():
    vol_name = sanitize_text(request.form.get("vol_name", ""))
    vol_email = sanitize_email(request.form.get("vol_email", ""))
    vol_number = sanitize_phone(request.form.get("vol_number", ""))
    vol_organization = sanitize_text(request.form.get("vol_organization", ""))
    vol_text = sanitize_text(request.form.get("vol_text", ""))

    if not all([vol_name, vol_number]) or not vol_email:
        flash("Name, email and phone number are required.", category="error")
        return redirect(url_for("volunteer"))

    # Check if email already registered as a volunteer
    existing_volunteer = VolunteerApplication.query.filter(
        db.func.lower(VolunteerApplication.email) == vol_email.lower()
    ).first()
    if existing_volunteer:
        flash("This email is already registered as a volunteer.", category="error")
        return redirect(url_for("volunteer"))

    try:
        new_volunteer = VolunteerApplication(
            name=vol_name,
            email=vol_email,
            number=vol_number,
            organization=vol_organization,
            message=vol_text
        )
        db.session.add(new_volunteer)
        db.session.commit()
        flash("Application sent successfully!", category="success")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash("Something went wrong. Please try again later.", category="error")

    return redirect(url_for("volunteer"))


@app.route("/get-in-touch/partners")
def partners():
    return render_template("public/partners.html")


@app.route("/get-in-touch/partners/sending-details", methods=["POST"])
def send_detail():
    part_name = sanitize_text(request.form.get("part_name", ""))
    part_email = sanitize_email(request.form.get("part_email", ""))
    part_number = sanitize_phone(request.form.get("part_number", ""))
    part_organization = sanitize_text(request.form.get("part_organization", ""))
    part_text = sanitize_text(request.form.get("part_text", ""))

    if not all([part_name, part_number]) or not part_email:
        flash("Name, email and phone number are required.", category="error")
        return redirect(url_for("partners"))

    # Check if email already registered as a partner
    existing_partner = PartnerApplication.query.filter(
        db.func.lower(PartnerApplication.email) == part_email.lower()
    ).first()
    if existing_partner:
        flash("This email is already registered as a partner.", category="error")
        return redirect(url_for("partners"))

    try:
        new_partner = PartnerApplication(
            name=part_name,
            email=part_email,
            number=part_number,
            organization=part_organization,
            message=part_text
        )
        db.session.add(new_partner)
        db.session.commit()
        flash("Application sent successfully!", category="success")
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        flash("Failed to send message. Please try again later.", category="error")

    return redirect(url_for("partners"))


@app.route("/donation")
def donate():
    return render_template("public/donation.html")


@app.route("/donation/paystack")
def paystack():
    return render_template("public/paystack.html")


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Session expired. Please try submitting the form again.", category="error")
    return redirect(request.referrer or url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.errorhandler(429)
def too_many_requests(e):
    flash("Too many requests. Please wait a moment and try again.", "error")
    return render_template("public/home.html", total_members=get_unique_member_count()), 429


@app.route('/donation/initialize', methods=['POST'])
@rate_limit(max_requests=5, window=60)  # 5 payment attempts/min per IP
def paystack_initialize():
    import requests as http_requests

    is_anonymous = bool(request.form.get('anonymous'))
    first_name = sanitize_text(request.form.get('firstName', ''))
    last_name = sanitize_text(request.form.get('lastName', ''))
    donor_name = f'{first_name} {last_name}'.strip() if not is_anonymous else 'Anonymous'
    donor_email = sanitize_email(request.form.get('email', ''))
    amount_ghs = sanitize_amount(request.form.get('amount', 0))

    # Validation
    if not donor_email:
        flash('Please enter a valid email address.', 'error')
        return redirect(url_for('donate'))

    if not amount_ghs:
        flash('Please enter a valid donation amount (min GH₵1, max GH₵100,000).', 'error')
        return redirect(url_for('donate'))

    if not is_anonymous and not first_name:
        flash('Please enter your name or choose anonymous donation.', 'error')
        return redirect(url_for('donate'))

    amount_pesewas = int(amount_ghs * 100)  # Paystack uses pesewas

    payload = {
        'email': donor_email,
        'amount': amount_pesewas,
        'currency': 'GHS',
        'metadata': {
            'donor_name': donor_name,
            'is_anonymous': is_anonymous,
            'custom_fields': [{
                'display_name': 'Donor Name',
                'variable_name': 'donor_name',
                'value': donor_name
            }]
        },
        'callback_url': url_for('paystack_callback', _external=True)
    }

    headers = {
        'Authorization': f'Bearer {os.getenv("PAYSTACK_SECRET_KEY")}',
        'Content-Type': 'application/json'
    }

    try:
        resp = http_requests.post(
            'https://api.paystack.co/transaction/initialize',
            json=payload, headers=headers, timeout=10
        )
        data = resp.json()
    except Exception:
        flash('Could not connect to payment provider. Please try again.', 'error')
        return redirect(url_for('donate'))

    if not data.get('status'):
        flash('Payment initialization failed. Please try again.', 'error')
        return redirect(url_for('donate'))

    donation = Donation(
        donor_name=donor_name,
        donor_email=donor_email,
        is_anonymous=is_anonymous,
        amount=amount_ghs,
        paystack_reference=data['data']['reference'],
        paystack_status='pending',
        is_verified=False
    )
    db.session.add(donation)
    db.session.commit()

    # Redirect directly to Paystack checkout
    return redirect(data['data']['authorization_url'])


@app.route('/donation/callback')
def paystack_callback():
    """Paystack redirects the user here after payment."""
    reference = request.args.get('trxref') or request.args.get('reference')
    if not reference:
        flash('No payment reference found.', 'error')
        return redirect(url_for('donate'))
    return redirect(url_for('paystack_verify', reference=reference))


@app.route('/donation/verify/<reference>')
def paystack_verify(reference):
    """
    Server-side verification — NEVER trust the client.
    Paystack sends the reference; we verify it against their API.
    """
    import requests as http_requests

    # Sanitize reference to prevent injection
    reference = re.sub(r'[^a-zA-Z0-9_\-]', '', reference)[:200]

    donation = Donation.query.filter_by(paystack_reference=reference).first()
    if not donation:
        flash('Donation record not found.', 'error')
        return redirect(url_for('donate'))

    # Prevent double processing
    if donation.is_verified:
        flash(f'Your donation of GH₵{donation.amount:,.2f} was already confirmed. Thank you! 🌿', 'success')
        return redirect(url_for('home'))

    headers = {'Authorization': f'Bearer {os.getenv("PAYSTACK_SECRET_KEY")}'}
    try:
        resp = http_requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers, timeout=10
        )
        data = resp.json()
    except Exception:
        flash('Could not verify payment. Please contact us if funds were deducted.', 'error')
        return redirect(url_for('home'))

    if data.get('status') and data['data']['status'] == 'success':
        donation.paystack_status = 'success'
        donation.is_verified = True
        donation.verified_at = datetime.now(timezone.utc)
        db.session.commit()
        display = 'Anonymous donor' if donation.is_anonymous else donation.donor_name
        flash(f'Thank you, {display}! Your donation of GH₵{donation.amount:,.2f} was received. 🌿', 'success')
    else:
        donation.paystack_status = data['data'].get('status', 'failed')
        db.session.commit()
        flash('Payment could not be verified. Please contact us if funds were deducted.', 'error')

    return redirect(url_for('home'))


@app.route('/donation/webhook', methods=['POST'])
def paystack_webhook():
    """
    Paystack server-to-server webhook.
    Add this URL in your Paystack dashboard → Settings → Webhooks:
        https://yourdomain.com/donation/webhook
    This runs even if the user closes their browser after paying.
    """
    paystack_secret = os.getenv('PAYSTACK_SECRET_KEY', '')
    signature = request.headers.get('X-Paystack-Signature', '')

    computed = hmac.new(
        paystack_secret.encode('utf-8'),
        request.data,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(computed, signature):
        return jsonify({'error': 'Invalid signature'}), 401

    event = request.get_json(silent=True)
    if not event:
        return jsonify({'error': 'Invalid payload'}), 400

    if event.get('event') == 'charge.success':
        ref = event['data'].get('reference', '')
        ref = re.sub(r'[^a-zA-Z0-9_\-]', '', ref)
        donation = Donation.query.filter_by(paystack_reference=ref).first()
        if donation and not donation.is_verified:
            donation.paystack_status = 'success'
            donation.is_verified = True
            donation.verified_at = datetime.now(timezone.utc)
            db.session.commit()

    return jsonify({'status': 'ok'}), 200