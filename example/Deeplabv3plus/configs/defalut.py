config = dict(
    model=dict(
        type='deeplabv3plus',
        params=dict(
            encoder=dict(
                type='deeplab_encoder',
                params=dict(
                    resnet_encoder=dict(
                        resnet_type='resnet50',
                        include_conv5=True,
                        batchnoram_trainable=False,
                        pretrained=False,
                        freeze_at=0,
                        output_stride=16,
                    ),
                    aspp=dict(
                        in_channel=2048,
                        aspp_dim=256,
                        atrous_rates=(6, 12, 18),
                        add_image_level=True,
                        use_bias=True,
                        use_batchnorm=False,
                        norm_type='batchnorm'
                    ),
                )
            ),
            decoder=dict(
                type='deeplab_decoder',
                params=dict(
                    low_level_feature_channel=256,
                    encoder_feature_channel=256,
                    reduction_dim=48,
                    decoder_dim=256,
                    num_3x3conv=2,
                    scale_factor=4.0,
                    use_bias=True,
                    use_batchnorm=False,
                    norm_fn='batchnorm',
                ),
            ),
            loss=dict(
                cls_loss=dict(
                    type='cross_entropy',
                    params=dict(
                        ignore_index=-100,
                        reduction='mean',
                    ),
                )
            ),
            other=dict(
                use_softmax=True,
                num_classes=20,
                scale_factor=4
            )
        )
    ),
    data=dict(
        train=dict(
            type='segdataloader',
            params=dict(
                image_dir='',
                mask_dir='',
                filenameList_path=None,
                training=True,
                image_format='jpg',
                mask_format='png',
                batch_size=2,
                num_workers=0,
                pin_memory=True,
                drop_last=False,
            ),
        ),
        test=dict(
            type='segdataloader',
            params=dict(
                image_dir='',
                mask_dir='',
                filenameList_path=None,
                training=False,
                image_format='jpg',
                mask_format='png',
                batch_size=1,
                num_workers=0,
                pin_memory=True,
                drop_last=False,
            ),
        )
    ),
    optimizer=dict(
        type='sgd',
        params=dict(
            lr=0.01,
            momentum=0.9,
            weight_decay=0.0001
        )
    ),
    learning_rate=dict(
        type='multistep',
        params=dict(
            base_lr=0.01,
            steps=(60000, 80000),
            gamma=0.1,
            warmup_step=500,
            warmup_init_lr=0.01 / 3, ),
    ),
    train=dict(
        forward_times=1,
        num_iters=90000,
    ),
    test=dict(
    ),
)
