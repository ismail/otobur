package ws.donmez.otobur;

import android.content.Context;
import android.graphics.Typeface;
import android.text.TextPaint;
import android.text.style.MetricAffectingSpan;

public class CustomFont extends MetricAffectingSpan {

	private static Typeface mTypeface;
	
	public CustomFont(Context context) {
		mTypeface = Typeface.createFromAsset(context.getAssets(), 
				"font/EHSMB.ttf");
	}

	@Override
	public void updateMeasureState(TextPaint p) {
		p.setTypeface(mTypeface);
	}

	@Override
	public void updateDrawState(TextPaint tp) {
		tp.setTypeface(mTypeface);
	}

}
