package ws.donmez.otobur;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Paint.Align;
import android.graphics.Typeface;
import android.text.TextPaint;
import android.text.style.MetricAffectingSpan;

public class CustomFont extends MetricAffectingSpan {

	private static Typeface mTypeface;
	
	public CustomFont(Context context) {
		mTypeface = Typeface.createFromAsset(context.getAssets(), 
				                             "font/ehsmb.ttf");
	}

	@Override
	public void updateMeasureState(TextPaint p) {
		p.setColor(Color.YELLOW);
		p.setTypeface(mTypeface);
	}

	@Override
	public void updateDrawState(TextPaint tp) {
		tp.setColor(Color.YELLOW);
		tp.setTypeface(mTypeface);
	}

}
