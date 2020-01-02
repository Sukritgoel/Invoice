if flag>=2:
        c = c_info[0]
        d=  c_info[1]
        print(c)
        print(d)
        del c_info[0]
        if c['x1']<d['x1']:
            min_x1=c['x1']
        else:
            min_x1=d['x1']

        if c['x2']>d['x2']:
            max_x2=c['x2']
        else:
            max_x2=d['x2']                           
        if c['y1']<d['y1']:
            min_y1=c['y1']
        else:
            min_y1=d['y1']

        if c['y2']>d['y2']:
            max_y2=c['y2']
        else:
            max_y2=d['y2']

        this_crop = min_x1,min_y1,max_x2,max_y2
        crop = this_crop
        covered_sum = c['sum']+d['sum']
        while covered_sum < total:
            changed = False
            recall = 1.0 * covered_sum / total
            prec = 1 - 1.0 * crop_area(crop) / area
            f1 = 2 * (prec * recall / (prec + recall))
            #print '----'
            for i, c in enumerate(c_info):
                this_crop = d['x1'], c['y1'], c['x2'], d['y2']
                new_crop = union_crops(crop, this_crop)
                new_sum = covered_sum + c['sum']+d['sum']
                new_recall = 1.0 * new_sum / total
                new_prec = 1 - 1.0 * crop_area(new_crop) / area
                new_f1 = 2 * new_prec * new_recall / (new_prec + new_recall)

                # Add this crop if it improves f1 score,
                # _or_ it adds 25% of the remaining pixels for <15% crop expansion.
                # ^^^ very ad-hoc! make this smoother
                remaining_frac = c['sum'] / (total - covered_sum)
                print(crop_area(crop))                                
                new_area_frac = 1.0 * crop_area(new_crop) / crop_area(crop) - 1
                if new_f1 > f1 or (
                        remaining_frac > 0.25 and new_area_frac < 0.15):
                    print('%d %s -> %s / %s (%s), %s -> %s / %s (%s), %s -> %s' % (
                            i, covered_sum, new_sum, total, remaining_frac,
                            crop_area(crop), crop_area(new_crop), area, new_area_frac,
                            f1, new_f1))
                    crop = new_crop
                    covered_sum = new_sum
                    del c_info[i]
                    changed = True
                    break

            if not changed:
                break

        return crop
    else:
        c=c_info[0]
        print(c)        

        this_crop = c['x1'],c['y1'],c['x2'],c['y2']
        crop = this_crop
        print(crop)
        covered_sum = c['sum']

        while covered_sum < total:
            changed = False
            recall = 1.0 * covered_sum / total
            prec = 1 - 1.0 * crop_area(crop) / area
            f1 = 2 * (prec * recall / (prec + recall))
            #print '----'
            for i, c in enumerate(c_info):
                this_crop = c['x1'],c['y1'],c['x2'],c['y2']
                new_crop = union_crops(crop, this_crop)
                new_sum = covered_sum + c['sum']
                new_recall = 1.0 * new_sum / total
                new_prec = 1 - 1.0 * crop_area(new_crop) / area
                new_f1 = 2 * new_prec * new_recall / (new_prec + new_recall)

                # Add this crop if it improves f1 score,
                # _or_ it adds 25% of the remaining pixels for <15% crop expansion.
                # ^^^ very ad-hoc! make this smoother
                remaining_frac = c['sum'] / (total - covered_sum)
                #print(crop_area(crop))
                new_area_frac = 1.0 * crop_area(new_crop) / crop_area(crop) - 1
                if new_f1 > f1 or (
                        remaining_frac > 0.25 and new_area_frac < 0.15):
                    print('%d %s -> %s / %s (%s), %s -> %s / %s (%s), %s -> %s' % (
                            i, covered_sum, new_sum, total, remaining_frac,
                            crop_area(crop), crop_area(new_crop), area, new_area_frac,
                            f1, new_f1))
                    crop = new_crop
                    covered_sum = new_sum
                    del c_info[i]
                    changed = True
                    break

            if not changed:
                break
